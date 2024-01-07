import sqlalchemy
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String,Float
import os,sys
# Defining path variables
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
root_path = os.path.dirname(__file__)
from models.houseprice import *


# Enironment Variables
from utils.load_env import load_env_file
load_env_file(".env")

# Lambda Funcs
sqlalchemytext = lambda x:sqlalchemy.text(x)

# 1. Connect to the database and check Connection
def test_connection(db_name = "sys"):
    # Database connection string for MariaDB
    db_username = os.getenv("DB_USERNAME")
    db_password = os.getenv("DB_PASSWORD")
    db_host = os.getenv("DB_HOST")
    db_port = os.getenv("DB_PORT")


    db_username = "root"
    db_password = "pswd"
    db_host = "localhost"
    db_port = "3306"

    db_connection_string = f"mariadb+pymysql://{db_username}:\
    {db_password}@{db_host}:{db_port}/{db_name}"

    # db_connection_string = f"mariadb+pymysql://{db_username}:\
    # {db_password}@{db_host}:{db_port}"

    try:
        # Create an SQLAlchemy engine
        engine = sqlalchemy.create_engine(db_connection_string)
        connection = engine.connect()
        connection.close()
        return True

    except Exception as e:
        print("Test Connection Exception:", e)
        return False

def create_db(db_name = "data"):
    db_username = os.getenv("DB_USERNAME")
    db_password = os.getenv("DB_PASSWORD")
    db_host = os.getenv("DB_HOST")
    db_port = os.getenv("DB_PORT")

    DATABASE_URI = f"mariadb+pymysql://{db_username}:{db_password}@{db_host}:{db_port}"
    DATABASE_NAME = db_name

    engine = sqlalchemy.create_engine(f"{DATABASE_URI}/{DATABASE_NAME}")
    if test_connection(db_name=DATABASE_NAME):
        print(f"Database '{DATABASE_NAME}' already exists.")
    else:
        try:
            engine = sqlalchemy.create_engine(DATABASE_URI)
            connection = engine.connect()
            connection.execute(sqlalchemytext("commit"))
            connection.execute(sqlalchemytext(f"CREATE DATABASE {DATABASE_NAME}"))
            # connection.execute(sqlalchemy.text("commit"))
            print(f"Database '{DATABASE_NAME}' created successfully.")
        except Exception as e:
            print(f"***Exception: {e}")
        finally:
            connection.close()
            engine.dispose()


def create_table(db_name = "data",table_name = "trainingData"):
    try:
        db_username = os.getenv("DB_USERNAME")
        db_password = os.getenv("DB_PASSWORD")
        db_host = os.getenv("DB_HOST")
        db_port = os.getenv("DB_PORT")

        DATABASE_URI = f"mariadb+pymysql://{db_username}:{db_password}@{db_host}:{db_port}/{db_name}"
        TABLE_NAME = table_name


        engine = create_engine(DATABASE_URI)
        metadata = MetaData()

        # Define your table structure
    #     final_cols = ['LotFrontage', 'LotArea', 'LotShape', 'OverallQual',
    #    'OverallCond', 'YearBuilt', 'YearRemodAdd', 'MasVnrArea', 'ExterQual',
    #    'BsmtFinSF1', 'BsmtUnfSF', 'TotalBsmtSF', 'CentralAir', '1stFlrSF',
    #    '2ndFlrSF', 'GrLivArea', 'BsmtFullBath', 'FullBath', 'HalfBath',
    #    'BedroomAbvGr', 'TotRmsAbvGrd', 'Fireplaces', 'GarageYrBlt',
    #    'GarageFinish', 'GarageCars', 'GarageArea', 'WoodDeckSF', 'OpenPorchSF',
    #    'EnclosedPorch', '3SsnPorch', 'ScreenPorch', 'PoolArea', 'MoSold',
    #    'YrSold']

        # ['LotShape', 'ExterQual', 'CentralAir', 'GarageFinish']
        # ['Reg' 'IR1' 'IR2' 'IR3']
        # ['Gd' 'TA' 'Ex' 'Fa']
        # ['Y' 'N']
        # ['RFn' 'Unf' 'Fin']

        your_table = Table(
            table_name,
            metadata,
            Column('id', Integer, primary_key=True),
            Column('MSSubClass', Integer), 
            Column('LotFrontage', Float), 
            Column('LotArea', Integer), 
            Column('LotShape', String(3)), 
            Column('OverallQual', Integer), 
            Column('OverallCond', Integer), 
            Column('YearBuilt', Integer), 
            Column('YearRemodAdd', Integer), 
            Column('MasVnrArea', Float), 
            Column('ExterQual', String(2)), 
            Column('BsmtFinSF1', Integer), 
            Column('BsmtUnfSF', Integer), 
            Column('TotalBsmtSF', Integer), 
            Column('CentralAir', String(1)), 
            Column('1stFlrSF', Integer), 
            Column('2ndFlrSF', Integer), 
            Column('GrLivArea', Integer), 
            Column('BsmtFullBath', Integer), 
            Column('FullBath', Integer), 
            Column('HalfBath', Integer), 
            Column('BedroomAbvGr', Integer), 
            Column('TotRmsAbvGrd', Integer), 
            Column('Fireplaces', Integer), 
            Column('GarageYrBlt', Float), 
            Column('GarageFinish', String(3)), 
            Column('GarageCars', Integer), 
            Column('GarageArea', Integer), 
            Column('WoodDeckSF', Integer), 
            Column('OpenPorchSF', Integer), 
            Column('EnclosedPorch', Integer), 
            Column('3SsnPorch', Integer), 
            Column('ScreenPorch', Integer), 
            Column('PoolArea', Integer), 
            Column('MoSold', Integer), 
            Column('YrSold', Integer), 
            Column('SalePrice', Integer)
        )

        # Check if the table exists, and create it if it doesn't
        metadata.create_all(engine, checkfirst=True)
        returnString = "Table {} Created in DB:{} Successfully.".format(table_name,db_name)

    except Exception as e:
        returnString = "***Exception {}".format(e)
    return returnString


def dropTable(db_name = "data", table_name = "trainingData"):
    try:
        db_username = os.getenv("DB_USERNAME")
        db_password = os.getenv("DB_PASSWORD")
        db_host = os.getenv("DB_HOST")
        db_port = os.getenv("DB_PORT")

        DATABASE_URI = f"mariadb+pymysql://{db_username}:{db_password}@{db_host}:{db_port}/{db_name}"
        TABLE_NAME = table_name

        engine = create_engine(DATABASE_URI)
        metadata = MetaData()

        # Replace 'your_table_name' with the actual name of the table you want to drop
        your_table = Table(table_name, metadata)

        # Drop the table
        your_table.drop(engine)
        returnString = "Table {} Droped from DB:{} Successfully.".format(table_name,db_name)

    except Exception as e:
        returnString = "***Exception {}".format(e)
    return returnString

def insertTrainingData(df,db_name = "data", table_name = "trainingData"):

    db_username = os.getenv("DB_USERNAME")
    db_password = os.getenv("DB_PASSWORD")
    db_host = os.getenv("DB_HOST")
    db_port = os.getenv("DB_PORT")

    DATABASE_URI = f"mariadb+pymysql://{db_username}:{db_password}@{db_host}:{db_port}/{db_name}"
    engine = sqlalchemy.create_engine(DATABASE_URI)

    try:

        with engine.connect() as connection:
            df.to_sql(name=table_name, con=connection, if_exists='append', index=False)
        returnString = "Inserted Values Successfully in {} in DB:{}.".format(table_name,db_name)
    except Exception as e:
        returnString = "***Exception {}".format(e)
    return returnString


if __name__ == "__main__":

    from time import sleep
    # print(test_connection())
    # create_db()

    print(create_table())
    train_path = "data/house-prices-advanced-regression-techniques/train.csv"
    df = preprocess_housing_df(train_path)
    print(insertTrainingData(df))

    for _ in range(10):
        temp_df = pd.read_csv(train_path).sample(10)[train_cols]
        print(insertTrainingData(temp_df))
        # sleep(1)

    # print(dropTable())
    # pass
    


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