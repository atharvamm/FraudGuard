from catboost import CatBoostRegressor
import pandas as pd
from flask import jsonify
import numpy as np

houseprice_model = None 

# Load Model from Checkpoint
def load_houseprice_model():
    global houseprice_model
    houseprice_model_path = 'models/checkpoints/housing_price_model.cbm'
    houseprice_model = CatBoostRegressor()
    houseprice_model.load_model(houseprice_model_path)

# Columns to use to make predictions
final_cols = ['MSSubClass', 'LotFrontage', 'LotArea', 'LotShape', 'OverallQual',
       'OverallCond', 'YearBuilt', 'YearRemodAdd', 'MasVnrArea', 'ExterQual',
       'BsmtFinSF1', 'BsmtUnfSF', 'TotalBsmtSF', 'CentralAir', '1stFlrSF',
       '2ndFlrSF', 'GrLivArea', 'BsmtFullBath', 'FullBath', 'HalfBath',
       'BedroomAbvGr', 'TotRmsAbvGrd', 'Fireplaces', 'GarageYrBlt',
       'GarageFinish', 'GarageCars', 'GarageArea', 'WoodDeckSF', 'OpenPorchSF',
       'EnclosedPorch', '3SsnPorch', 'ScreenPorch', 'PoolArea', 'MoSold',
       'YrSold']

def valid_vals(ip_data):
    "Check if the numerical and categorical value for ip_data is in the valid range for respective column."
    pass


# Check if the data type in the request is correct
def check_dtypes(ip_data):
    string_cols = "LotShape","ExterQual","CentralAir","GarageFinish"

    numeric_cols = ["MSSubClass", "LotFrontage", "LotArea", "OverallQual", "OverallCond","YearBuilt", "YearRemodAdd", "MasVnrArea", "BsmtFinSF1", "BsmtUnfSF","TotalBsmtSF", "1stFlrSF", "2ndFlrSF", "GrLivArea", "BsmtFullBath","FullBath", "HalfBath", "BedroomAbvGr", "TotRmsAbvGrd", "Fireplaces","GarageYrBlt", "GarageCars", "GarageArea", "WoodDeckSF", "OpenPorchSF","EnclosedPorch", "3SsnPorch", "ScreenPorch", "PoolArea", "MoSold","YrSold"]

    val_errors = []
    for col in string_cols:
        if not isinstance(ip_data.loc[0,col],str):
            val_errors.append("Value in "+col+" not of type string.")

    temp = pd.to_numeric(ip_data.iloc[0],errors="coerce")   
    
    for col,val in list(zip(temp.index,temp.values)):
        if np.isnan(val):
            if col in string_cols:
                continue
            else:
                val_errors.append("Value in "+ col +" is not real number.")
    if len(val_errors):
        return False,"\n".join(val_errors)
    return True,""

# Check the data before predicting
def houseprice_datachecks(ip_data):
    if not(all(ip_data.columns == final_cols)):
        return False,"Not all columns available"
    dtypes,message = check_dtypes(ip_data)
    if not dtypes:
        return False,message
    return True,""

# Use loaded model to predict houseprice
def predict_houseprice(data):
    datacheck_status,message = houseprice_datachecks(data)
    if datacheck_status:
        prediction = houseprice_model.predict(data)
        return jsonify({'prediction': prediction.tolist()[0]})
    else:
        return jsonify({'error': str(message)})

# Generate random data point
def generate_sample_houseprice_points(df,num_samples = 100):
    bootstrapped_samples = []

    for _ in range(num_samples):
        bootstrap_sample = {col: df[col].sample(n=1).values[0] for col in df.columns}
        bootstrapped_samples.append(bootstrap_sample)

    return pd.DataFrame(bootstrapped_samples)







     