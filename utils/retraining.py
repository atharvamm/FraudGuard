# Defining path variables
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

# from utils.load_env import load_env_file
import os
from models.houseprice import *
import pandas as pd
import logging
import sqlalchemy
from catboost import CatBoostRegressor
from utils.load_env import load_env_file
load_env_file(".env")

def retraining_model(db_name = "data",table_name = "trainingData"):
    db_username = os.getenv("DB_USERNAME")
    db_password = os.getenv("DB_PASSWORD")
    db_host = os.getenv("DB_HOST")
    db_port = os.getenv("DB_PORT")

    DATABASE_URI = f"mariadb+pymysql://{db_username}:{db_password}@{db_host}:{db_port}/{db_name}"
    TABLE_NAME = table_name

    engine = sqlalchemy.create_engine(DATABASE_URI)

    with engine.connect() as connection:
            df = pd.read_sql(TABLE_NAME, con=connection)
    df = df[train_cols]
    df.dropna(inplace=True,how="any")
    non_numeric_columns = df.select_dtypes(exclude=['number']).columns.tolist()

    train_data = df.drop(columns="SalePrice")
    train_labels = df["SalePrice"]
    model = CatBoostRegressor(iterations=10,
                            learning_rate=1,
                            depth=16,
                            verbose = False,
                            cat_features = non_numeric_columns,
                            )

    model.fit(train_data, train_labels)
    model_path = 'models/checkpoints//check_retraing.cbm'
    # model.save_model(os.path.join(root_path,model_path))
    logging.info(f"Model saved to {model_path}")
