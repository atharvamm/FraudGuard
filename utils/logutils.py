import logging
from flask import request


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



def log_response_info(response):
    # Log response information after processing the request
    log_data = {
        'status_code': response.status_code,
        'response_data': response.data.decode('utf-8'),
        'host_addr': request.host,
    }
    logging.info(f'Response: {log_data}')
    # return response