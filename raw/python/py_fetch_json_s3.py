import requests

def fetch_json(url):
    # Send an HTTP GET request to the specified URL
    response = requests.get(url)
    
    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse the JSON content from the response
        json_data = response.json()
        return json_data
    else:
        # Return None or handle the error according to your requirements
        print(f"Failed to retrieve data. Status code: {response.status_code}")
        return None

# Example usage
url = "https://api.example.com/data"
json_result = fetch_json(url)
if json_result is not None:
    print(json_result)
