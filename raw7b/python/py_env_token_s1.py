import os

def get_api_token():
    # Retrieve the API_TOKEN from the environment variables
    return os.getenv("API_TOKEN")
