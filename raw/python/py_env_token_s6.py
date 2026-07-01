import os

def get_api_token():
    # Retrieve the API_TOKEN from the environment variables
    api_token = os.getenv('API_TOKEN')
    
    # Check if the API_TOKEN is not None or empty
    if api_token:
        return api_token
    else:
        raise ValueError("The API_TOKEN environment variable is not set.")
