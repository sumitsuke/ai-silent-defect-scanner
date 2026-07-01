import os

def get_api_token():
    # Retrieve the API token from the environment variable
    api_token = os.getenv('API_TOKEN')
    
    # Check if the API token is not None before returning it
    if api_token is not None:
        return api_token
    else:
        raise ValueError("Environment variable API_TOKEN is not set.")
