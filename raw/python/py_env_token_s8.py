import os

def get_api_token():
    # Retrieve the API token from the environment variable
    api_token = os.getenv('API_TOKEN')
    
    if api_token is None:
        raise ValueError("API_TOKEN environment variable not set")
    
    return api_token
