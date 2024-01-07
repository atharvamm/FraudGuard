# Defining path variables
import os
import sys
sys.path.append(os.path.dirname(__file__))
root_path = os.path.dirname(__file__)

## Imports
from utils.load_env import load_env_file
from utils.fileops import delete_files_in_directory
from models.houseprice import *
import logging



# Load files and models
load_env_file(".env")
def load_models():
    load_houseprice_model()
load_models()


# Clean Logs
delete_files_in_directory(os.path.join(root_path,"logs"))


# Logging
if bool(os.getenv("FLASK_DEBUG")):
    logfpath = os.path.join(root_path,'logs','dev.log')
    logging.basicConfig(filename = logfpath, level=logging.DEBUG,
                        format='%(asctime)s [%(levelname)s] - %(message)s')
else:
    logfpath = os.path.join(root_path,'logs','prod.log')
    logging.basicConfig(filename = logfpath, level=logging.INFO,
                        format='%(asctime)s [%(levelname)s] - %(message)s')