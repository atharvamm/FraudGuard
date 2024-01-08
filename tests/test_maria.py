import os,sys
# Defining path variables
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
root_path = os.path.dirname(__file__)
from models.houseprice import *
from utils.dbops import *


def test_connection(DB_NAME = "sys"):
    try:
        engine = connectMariaDb(DB_NAME)
        connection = engine.connect()
        connection.close()
        return True

    except Exception:
        return False


if __name__ == "__main__":

    dropTableMariaDb()
    createDatabaseMariaDb()
    createTableMariaDb()

    train_path = "data/house-prices-advanced-regression-techniques/train.csv"
    df = preprocess_housing_df(train_path)
    insertTrainingDataMariaDb(df)
    for _ in range(10):
        temp_df = pd.read_csv(train_path).sample(10)[train_cols]
        print(insertTrainingDataMariaDb(temp_df))

    # dropTableMariaDb()    


# def template(db_name = "data", table_name = "trainingData"):

#     db_username = os.getenv("DB_USERNAME")
#     db_password = os.getenv("DB_PASSWORD")
#     db_host = os.getenv("DB_HOST")
#     db_port = os.getenv("DB_PORT")

#     DATABASE_URI = f"mariadb+pymysql://{db_username}:{db_password}@{db_host}:{db_port}/{db_name}"

#     try:
#         returnString = "Table {} Droped from DB:{} Successfully.".format(table_name,db_name)
#     except Exception as e:
#         returnString = "***Exception {}".format(e)
#     return returnString