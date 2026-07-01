import requests

def fetch_json(url):
    response = requests.get(url)
    
    # Check if the request was successful
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Failed to retrieve JSON from {url}. Status code: {response.status_code}")
