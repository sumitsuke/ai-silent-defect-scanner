import os

def get_api_token():
    """
    Returns the API token from the environment variable API_TOKEN.
    
    Returns:
        str: The API token if set, otherwise None.
    """
    return os.getenv("API_TOKEN")
