import requests

def fetch_json(url):
    # Send an HTTP GET request to the specified URL
    response = requests.get(url)
    
    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse the JSON content of the response into a Python dictionary
        json_data = response.json()
        return json_data
    else:
        # If the request failed, raise an exception with the status code and error message
        raise Exception(f"Failed to fetch data from {url}. Status code: {response.status_code}, Error: {response.text}")
