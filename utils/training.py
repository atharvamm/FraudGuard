# Defining path variables
import os
import sys
root_path = os.path.dirname(os.path.dirname(__file__))
sys.path.append(root_path)

from datetime import datetime
from models.houseprice import *
import pandas as pd
import logging
from catboost import CatBoostRegressor
from utils.load_env import load_env_file
load_env_file(".env")
from utils.dbops import *

def trainHousePriceModel(DB_NAME = "data",TABLE_NAME = "trainingData"):

    engine = connectMariaDb(DB_NAME)

    with engine.connect() as connection:
            df = pd.read_sql(TABLE_NAME, con=connection)
    df = df[train_cols]
    df.dropna(inplace=True,how="any")
    non_numeric_columns = df.select_dtypes(exclude=['number']).columns.tolist()

    train_data = df.drop(columns="SalePrice")
    train_labels = df["SalePrice"]
    model = CatBoostRegressor(iterations=100,
                            learning_rate=1,
                            depth=16,
                            verbose = False,
                            cat_features = non_numeric_columns,
                            )

    model.fit(train_data, train_labels)

    lastModel = getLastModel()

    if isinstance(lastModel,list) and len(lastModel) > 0:
      version_list = lastModel[0]["version"].split('.')
      cur_version = str(int(version_list[-1])+1)
      version_str = version_list[0]+"."+cur_version
      path_list = lastModel[0]["model_path"].split('.')
      model_path = path_list[0].split("_")[0]+'_'+cur_version+'.'+path_list[-1]

    else:
        version_str = "v1.0"
        model_path = 'models/checkpoints/housePrice_0.cbm'

    model.save_model(os.path.join(root_path,model_path))
    model_dict = {
         'modelType': 'prod',
          "version" : version_str,
          "timestamp" : str(datetime.now()),
          "model_path" : model_path,
          "eval_result" : model.evals_result_,
          "params" : model.get_all_params()
    }

    insertResponse = dynamoInsertItem(model_dict)
    # logging.info(insertResponse)
    logging.info(f"Model saved to {model_path}")

    load_houseprice_model()






if __name__ == "__main__":
  deleteDynamoTable()
  createDynamoTable()
  # trainHousePriceModel()
  # trainHousePriceModel()