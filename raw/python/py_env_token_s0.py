import os

def get_api_token():
    # Check if the API_TOKEN environment variable exists
    if 'API_TOKEN' in os.environ:
        return os.getenv('API_TOKEN')
    else:
        raise ValueError("The API_TOKEN environment variable is not set.")
