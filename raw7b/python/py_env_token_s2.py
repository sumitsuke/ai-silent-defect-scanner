import os

def get_api_token():
    """
    Retrieves the API token from the environment variable.

    Returns:
        str: The API token if it exists, otherwise an empty string.
    """
    return os.getenv('API_TOKEN', '')
