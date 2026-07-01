import requests

def fetch_json(url):
    # Perform an HTTP GET request to the specified URL
    response = requests.get(url)
    
    # Check if the request was successful
    if response.status_code == 200:
        # Parse the JSON body and return it as a dictionary
        return response.json()
    else:
        # Return None if the request failed
        return None

# Example usage of the function
if __name__ == "__main__":
    url = "https://api.example.com/data"
    data = fetch_json(url)
    print(data)
