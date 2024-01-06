import requests
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from models.houseprice import generate_sample_houseprice_points
import pandas as pd
import time
import random
from flask import jsonify
import json

# Initial test to check if successful connection
def test_local_service(host, port):
    url = f"http://{host}:{port}/test"
    
    try:
        response = requests.get(url)
        
        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            print(f"Request successful. Response content: {response.text}")
        else:
            print(f"Request failed with status code: {response.status_code}")
    except requests.RequestException as e:
        print(f"Error making request: {e}")

# Randomly generate data and then get predictions.
def test_house_price_model(host,port,samples = 100):
    final_cols = ['MSSubClass', 'LotFrontage', 'LotArea', 'LotShape', 'OverallQual',
       'OverallCond', 'YearBuilt', 'YearRemodAdd', 'MasVnrArea', 'ExterQual',
       'BsmtFinSF1', 'BsmtUnfSF', 'TotalBsmtSF', 'CentralAir', '1stFlrSF',
       '2ndFlrSF', 'GrLivArea', 'BsmtFullBath', 'FullBath', 'HalfBath',
       'BedroomAbvGr', 'TotRmsAbvGrd', 'Fireplaces', 'GarageYrBlt',
       'GarageFinish', 'GarageCars', 'GarageArea', 'WoodDeckSF', 'OpenPorchSF',
       'EnclosedPorch', '3SsnPorch', 'ScreenPorch', 'PoolArea', 'MoSold',
       'YrSold']
    
    # Read data from path and process data.
    path = "data/house-prices-advanced-regression-techniques/train.csv"
    df = pd.read_csv(os.path.join(path))
    df = df[final_cols]
    df.dropna(inplace=True,how="any")    
    sample_df = generate_sample_houseprice_points(df,samples)

    pred = 10
    # Get predictions pred times
    for _ in range(pred):
        time.sleep(random.randint(0,10))

        url = f"http://{host}:{port}/house-price"    
        try:
            sample_json = sample_df.sample(n=1).to_json(orient="records")
            headers = {'Content-Type': 'application/json'}
            response = requests.post(url, data=sample_json, headers=headers)

            if response.status_code == 200:
                print(f"Request successful. Response content: {response.text}")
            else:
                print(f"Request failed with status code: {response.status_code}")
        except requests.RequestException as e:
            print(f"Error making request: {e}")


def test_authenticate_component(host,port,uname = "john_doe",pswd = "password123"):
    login_url = f"http://{host}:{port}/login"
    protected_url = f"http://{host}:{port}/protected"

    login_response = requests.post(login_url,json={"username":str(uname),"password":str(pswd)})

    if login_response.status_code == 200:
        token = login_response.json()["token"]
        headers = {"Authorization":token}
        protected_response = requests.get(protected_url,headers=headers)
        if protected_response.status_code == 200:
            print(protected_response.json())



if __name__ == "__main__":
    host = False
    if host:
        from utils.load_env import load_env_file
        load_env_file(".env")
        host = os.getenv("REMOTE_HOST")
    else:
        host = "localhost"
    # test_local_service(host, 5000)
    # test_house_price_model(host, 8000,samples=10)
    test_authenticate_component(host,5000)

