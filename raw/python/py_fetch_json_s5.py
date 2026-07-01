import requests

def fetch_json(url):
    # Send an HTTP GET request to the provided URL
    response = requests.get(url)
    
    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse the JSON content of the response body
        json_data = response.json()
        
        # Return the parsed JSON data as a dictionary
        return json_data
    else:
        # Raise an exception if the request was not successful
        raise Exception(f"Failed to retrieve JSON data: {response.status_code}")
