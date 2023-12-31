# FraudGuard

Machine Learning model as a flask service to predict housing price given categorical and numerical features.
The model was trained using CatBoost. 

## Environment
The .yml file to create the environment is in utils directory.

## To run the code 
1. Clone the repo `git clone https://github.com/atharvamm/FraudGuard.git`
2. Create environment from .yml file `conda env create -f utils/fraudguard.yml`
3. Create an .env file with the following variables
    ```
    FLASK_DEBUG=True/False
    FLASK_RUN_HOST=Address of the host 127.0.0.1/0.0.0.0
    FLASK_RUN_PORT= Port to run on
    ALLOWED_IPS= IPs allowed to request service
    REMOTE_HOST= Remote host so that you can test the service.
    ```
This should setup and run the code.

## To test the code
Follow the above steps and run `test_requests.py` in tests directory. It should first run a test to see if it is able to connect to the server. And then generate sample datapoints to get predictions.