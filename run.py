from utils.load_env import load_env_file
from flask import Flask,url_for,request,jsonify
import os
import signal
import sys
from models.houseprice import predict_houseprice,load_houseprice_model
import pandas as pd
import logging
from utils.fileops import delete_files_in_directory

# Defining path variables
sys.path.append(os.path.dirname(__file__))
root_path = os.path.dirname(__file__)

# Clean Logs
delete_files_in_directory(os.path.join(root_path,"logs"))
# Clean DBs

# '''
# Logging
if bool(os.getenv("FLASK_DEBUG")):
    logfpath = os.path.join(root_path,'logs','dev.log')
    logging.basicConfig(filename = logfpath, level=logging.DEBUG,
                        format='%(asctime)s [%(levelname)s] - %(message)s')
else:
    logfpath = os.path.join(root_path,'logs','prod.log')
    logging.basicConfig(filename = logfpath, level=logging.INFO,
                        format='%(asctime)s [%(levelname)s] - %(message)s')


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


# App Logging
@app.before_request
def log_request_info():
    # Log request information before processing the request
    log_data = {
        'method': request.method,
        'path': request.path,
        'query_string': request.query_string,
        'data': request.data.decode('utf-8'),
        'remote_addr': request.remote_addr,
        'user_agent': request.headers.get('User-Agent'),
    }
    logging.info(f'Request: {log_data}')

# Define function to check ip
@app.before_request
def check_ip_access():
    if not is_ip_allowed():
        return jsonify({'error': 'Access denied. IP address not allowed.'}), 403

@app.after_request
def log_response_info(response):
    # Log response information after processing the request
    log_data = {
        'status_code': response.status_code,
        'response_data': response.data.decode('utf-8'),
        'host_addr': request.host,
    }
    logging.info(f'Response: {log_data}')
    return response


# Background model training


#### Services

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