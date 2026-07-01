import requests

def fetch_json(url):
    """
    Fetches data from a given URL and parses it as JSON.

    Args:
        url (str): The URL to fetch data from.

    Returns:
        dict: A dictionary containing the parsed JSON body.
    """
    # Send an HTTP GET request to the specified URL
    response = requests.get(url)
    
    # Check if the request was successful
    if response.status_code == 200:
        # Parse the JSON content of the response
        data = response.json()
        return data
    else:
        # Raise an exception if the request failed
        raise Exception(f"Failed to fetch data from {url}. Status code: {response.status_code}")
