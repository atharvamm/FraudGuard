import os,sys,json
from datetime import datetime
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from utils.load_env import load_env_file
from utils.dbops import *
load_env_file(".env")


if __name__ == "__main__":
    print(deleteDynamoTable())
    print(createDynamoTable())
    item_data = {
    'modelType': 'prod',
    'version': 'v1.0',
    'timestamp': str(datetime.now()), 
    'model_path': 'https://example.com/model1',
    'eval_result': {'accuracy': 0.95, 'precision': 0.85},
    'params': {'param1': 'value1', 'param2': 'value2'}
    }
    print(dynamoInsertItem(item_data))
    items_to_insert = [
    {
        'modelType': 'prod',
        'version': 'v1.1',
        'timestamp': str(datetime.now()),
        'model_path': 'https://example.com/model1',
        'eval_result': {'accuracy': 0.95, 'precision': 0.85},
        'params': {'param1': 'value1', 'param2': 'value2'}
    },
    {   
        'modelType': 'prod',
        'version': 'v1.2',
        'timestamp': str(datetime.now()),
        'model_path': 'https://example.com/model2',
        'eval_result': {'accuracy': 0.92, 'precision': 0.88},
        'params': {'param1': 'value3', 'param2': 'value4'}
    }
    ]
    print(insertDynamoBatchItems(items_to_insert))
    item_data = {
    'modelType': 'prod',
    'version': 'v1.3',
    'timestamp': str(datetime.now()), 
    'model_path': 'https://example.com/model1',
    'eval_result': {'accuracy': 0.95, 'precision': 0.85},
    'params': {'param1': 'value1', 'param2': 'value2'}
    }
    print(dynamoInsertItem(item_data))
    print(getLastModel())