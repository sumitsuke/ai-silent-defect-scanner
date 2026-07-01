import os

def get_api_token():
    # Check if the API_TOKEN environment variable is set
    api_token = os.getenv('API_TOKEN')
    
    # Return the API token if it exists, otherwise raise an exception
    if api_token:
        return api_token
    else:
        raise ValueError("The API_TOKEN environment variable is not set.")
