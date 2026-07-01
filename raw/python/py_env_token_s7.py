import os

def get_api_token():
    # Get the API token from the environment variable
    api_token = os.getenv('API_TOKEN')
    
    # Check if the API token is not None and return it
    if api_token:
        return api_token
    else:
        raise ValueError("The API_TOKEN environment variable is not set.")
