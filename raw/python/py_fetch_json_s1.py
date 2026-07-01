import requests

def fetch_json(url):
    response = requests.get(url)
    response.raise_for_status()  # Raise an exception for bad responses
    
    # Parse the JSON content from the response
    json_data = response.json()
    
    return json_data
