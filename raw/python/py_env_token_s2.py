import os

def get_api_token():
    """
    This function retrieves the API token from the environment variable API_TOKEN.
    
    Returns:
        str: The API token stored in the environment variable.
    """
    # Retrieve the API token from the environment variable
    api_token = os.getenv('API_TOKEN')
    
    # Check if the environment variable is set and return it, otherwise raise an exception
    if api_token is None:
        raise ValueError("Environment variable API_TOKEN is not set.")
    else:
        return api_token
