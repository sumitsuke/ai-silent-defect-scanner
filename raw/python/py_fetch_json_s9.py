import requests

def fetch_json(url):
    # Send an HTTP GET request to the specified URL
    response = requests.get(url)
    
    # Check if the request was successful (HTTP status code 200)
    if response.status_code == 200:
        # Parse the JSON content from the response
        json_data = response.json()
        
        return json_data
    else:
        # Return None if the request failed or returned a non-JSON body
        return None

# Example usage
url = "https://api.example.com/data"
data = fetch_json(url)
print(data)
