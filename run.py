from utils.load_env import load_env_file
from flask import Flask,url_for,request,jsonify
import os
import signal
import sys
from models.houseprice import predict_houseprice,load_houseprice_model
import pandas as pd

sys.path.append(os.path.dirname(__file__))


# '''
# Cleanup before exiting app
def cleanup(signum, frame):
    print(f"Received signal {signum}. Cleaning up before shutting down...")
    # Add your cleanup logic here
    sys.exit(0)
signal.signal(signal.SIGTERM, cleanup)

# Load files and models
load_env_file(".env")
def load_models():
    load_houseprice_model()
load_models()

# Only allow requests from ips in .env file
allowed_ips = os.getenv("ALLOWED_IPS").split(",")
def is_ip_allowed():
    global allowed_ips
    client_ip = request.remote_addr
    return client_ip in allowed_ips

# Create app
app = Flask(__name__)

# Define function to check ip
@app.before_request
def check_ip_access():
    if not is_ip_allowed():
        return jsonify({'error': 'Access denied. IP address not allowed.'}), 403

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


if __name__ == '__main__':
    try:
        app.run(
            host=os.getenv("FLASK_RUN_HOST"),
            port=os.getenv("FLASK_RUN_PORT"),
            debug=os.getenv("FLASK_DEBUG")
        )
    except KeyboardInterrupt:
        # Handle Ctrl+C (keyboard interrupt) gracefully
        cleanup(signal.SIGINT, None)
# '''