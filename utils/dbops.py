import boto3,os,sys,json,sqlalchemy
from datetime import datetime
from boto3.dynamodb.conditions import Key
from utils.load_env import load_env_file
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String,Float

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
load_env_file(".env")

######    DynamoDB    ######

# Establish Connection
def connectDynamoDb():
    try:
        dynamodb = boto3.resource('dynamodb', region_name='localhost', endpoint_url=f'http://{os.getenv("DYNAMO_HOST")}:{os.getenv("DYNAMO_PORT")}',
                                aws_access_key_id=os.getenv("ACCESS_KEY_ID"), aws_secret_access_key=os.getenv("SECRET_ACCESS_KEY"))
        return dynamodb
    except:
        raise ConnectionError("Unable to connect to DynamoDB")

# Create DynamoDB Table
def createDynamoTable(table_name = "modelData"):
    try :
        dynamodb = connectDynamoDb()

        # Define table schema
        attribute_definitions = [
            {'AttributeName': 'modelType', 'AttributeType': 'S'},
            {'AttributeName': 'timestamp', 'AttributeType': 'S'},
        ]

        key_schema = [
            {'AttributeName': 'modelType', 'KeyType': 'HASH'},  # Partition key
            {'AttributeName': 'timestamp', 'KeyType': 'RANGE'}, # Sort key
        ]

        # Define provisioned throughput
        provisioned_throughput = {
            'ReadCapacityUnits': 5,
            'WriteCapacityUnits': 5,
        }

        # Create table
        table = dynamodb.create_table(
            TableName=table_name,
            KeySchema=key_schema,
            AttributeDefinitions=attribute_definitions,
            ProvisionedThroughput=provisioned_throughput
        )

        table.wait_until_exists()

        return f"Table {table_name} created successfully, with {table.item_count} documents."
    except Exception as e:
        return f"Unable to create table in DynamoDB because:{e}."


# Insert Item in Table
def dynamoInsertItem(item_data,table_name = 'modelData'):
    try:
        dynamodb = connectDynamoDb()

        table = dynamodb.Table(table_name)
        table.put_item(
        Item={
            'modelType': item_data.get('modelType','dev'),
            'version': item_data.get('version','0.0'),
            'timestamp': str(item_data.get('timestamp',datetime.now())),
            'model_path': item_data.get('model_path',""),
            'eval_result': json.dumps(item_data.get('eval_result',{})),
            'params': json.dumps(item_data.get('params',{}))
            }
        )
        return f"Item inserted successfully."
        
    except Exception as e:
        return f"Unable to insert data in table because:{e}."


# Insert items in batches in Table
def insertDynamoBatchItems(items_to_insert,table_name = "modelData"):
    try:
        dynamodb = connectDynamoDb()
        table = dynamodb.Table(table_name)

        with table.batch_writer() as batch:
            for item_data in items_to_insert:
                batch.put_item(
                    Item={
                        'modelType': item_data.get('modelType','dev'),
                        'version': item_data.get('version','0.0'),
                        'timestamp': str(item_data.get('timestamp',datetime.now())),
                        'model_path': item_data.get('model_path',""),
                        'eval_result': json.dumps(item_data.get('eval_result',{})),
                        'params': json.dumps(item_data.get('params',{}))
                    }
                )
        return f"Items inserted successfully."
    except Exception as e:
        return f"Unable to insert data in table because:{e}."


# Get the last trained model
def getLastModel(table_name = "modelData"):
    try:
        dynamodb = connectDynamoDb()
        table = dynamodb.Table(table_name)

        response = table.query(
            KeyConditionExpression = Key('modelType').eq('prod'), ScanIndexForward=False,
            Limit=1)
        return response["Items"]
    except Exception as e:
        return str(e)


# Delete DyanmoDB Table    
def deleteDynamoTable(table_name = "modelData"):
    try:
        dynamodb = connectDynamoDb()
        table = dynamodb.Table(table_name)
        table.delete()
        return f"Table {table_name} deleted successfully."
    except Exception as e:
        return e









######    MariaDB    ######

### Lambda Functions
sqlalchemytext = lambda x:sqlalchemy.text(x)


def connectMariaDb(DB_NAME = None):
    try:
        db_username = os.getenv("DB_USERNAME")
        db_password = os.getenv("DB_PASSWORD")
        db_host = os.getenv("DB_HOST")
        db_port = os.getenv("DB_PORT")
        DATABASE_URI = f"mariadb+pymysql://{db_username}:{db_password}@{db_host}:{db_port}"

        if DB_NAME is None:
            engine = sqlalchemy.create_engine(DATABASE_URI)
        else:
            engine = sqlalchemy.create_engine(f"{DATABASE_URI}/{DB_NAME}")

        return engine
    except:
        raise ConnectionError("Unable to connect to MariaDB")


def createDatabaseMariaDb(DATABASE_NAME = "data"):
    engine = connectMariaDb(DATABASE_NAME)
    try:
        engine = connectMariaDb()
        connection = engine.connect()
        connection.execute(sqlalchemytext("commit"))
        connection.execute(sqlalchemytext(f"CREATE DATABASE {DATABASE_NAME}"))
        return f"Database '{DATABASE_NAME}' created successfully."
    except Exception as e:
        return f"***Exception: {e}"
    finally:
        connection.close()
        engine.dispose()


def createTableMariaDb(DB_NAME = "data",TABLE_NAME = "trainingData"):
    try:
        engine = connectMariaDb(DB_NAME)
        metadata = MetaData()

        your_table = Table(
            TABLE_NAME,
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

        metadata.create_all(engine, checkfirst=True)
        return "Table {} Created in DB:{} Successfully.".format(TABLE_NAME,DB_NAME)
    except Exception as e:
        return "***Exception {}".format(e)


def dropTableMariaDb(DB_NAME = "data", TABLE_NAME = "trainingData"):
    try:
        engine = create_engine(DB_NAME)
        metadata = MetaData()

        your_table = Table(TABLE_NAME, metadata)

        your_table.drop(engine)
        returnString = "Table {} Droped from DB:{} Successfully.".format(TABLE_NAME,DB_NAME)

    except Exception as e:
        returnString = "***Exception {}".format(e)
    return returnString


def insertTrainingDataMariaDb(df,DB_NAME = "data", TABLE_NAME = "trainingData"):
    engine = connectMariaDb(DB_NAME)
    try:
        with engine.connect() as connection:
            df.to_sql(name=TABLE_NAME, con=connection, if_exists='append', index=False)
        return "Inserted Values Successfully in {} in DB:{}.".format(TABLE_NAME,DB_NAME)
    except Exception as e:
        return "***Exception {}".format(e)

