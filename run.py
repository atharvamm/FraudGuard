from setup import *
# from utils.training import *
# from apscheduler.schedulers.background import BackgroundScheduler
from flask import Flask,request,jsonify
import signal
from models.houseprice import *
import pandas as pd
# import atexit
from utils.logutils import *

# '''
# Cleanup before exiting app
def cleanup(signum, frame):
    print(f"Received signal {signum}. Cleaning up before shutting down...")
    # Add your cleanup logic here
    sys.exit(0)
signal.signal(signal.SIGTERM, cleanup)


# Only allow requests from ips in .env file
allowed_ips = os.getenv("ALLOWED_IPS").split(",")
def is_ip_allowed():
    global allowed_ips
    client_ip = request.remote_addr
    return client_ip in allowed_ips

# Create app
app = Flask(__name__)

# Scheduler Object
# scheduler = BackgroundScheduler(max_instances = 1,daemon = True)
# scheduler.add_job(trainHousePriceModel, 'interval', seconds = 60,kwargs={"DB_NAME": "data","TABLE_NAME" : "trainingData"})
# atexit.register(lambda: scheduler.shutdown())

# App Logging
@app.before_request
def log_request_info_app():
    log_request_info()

# Define function to check ip
@app.before_request
def check_ip_access():
    if not is_ip_allowed():
        return jsonify({'error': 'Access denied. IP address not allowed.'}), 403

@app.after_request
def log_response_info_app(response):
    # Log response information after processing the request
    log_response_info(response)
    return response

#### Services ####

# Test route
@app.route("/test")
def hello():
    return "Welcome to Fraud Guard!!!"

# House price model service
@app.route("/house-price",methods = ["POST"])
def house_price():
    if request.method == "POST":
        try:
            data = request.get_json()
            df = pd.DataFrame(data)
            return predict_houseprice(df)
        except Exception as e:
            return jsonify({'error': str(e)})
    else:
        return jsonify({'error': 'Only POST requests are allowed for this endpoint'})


# scheduler.start()

if __name__ == '__main__':
    try:
        app.run(
            host=os.getenv("FLASK_RUN_HOST"),
            port=os.getenv("FLASK_RUN_PORT"),
            debug = "True" == os.getenv("FLASK_DEBUG")
        )
    except KeyboardInterrupt:
        cleanup(signal.SIGINT, None)
# '''