import requests

def fetch_json(url):
    # Send a GET request to the specified URL
    response = requests.get(url)
    
    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse the JSON content from the response
        data = response.json()
        return data
    else:
        # Return None if the request failed
        return None

# Example usage
url = "https://api.example.com/data"
json_data = fetch_json(url)
if json_data:
    print(json_data)
else:
    print("Failed to retrieve JSON data")
