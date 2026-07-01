import os

def get_api_token():
    """
    Returns the API token stored in the environment variable API_TOKEN.
    
    Returns:
        str: The API token if it exists, otherwise None.
    """
    api_token = os.getenv('API_TOKEN')
    return api_token
