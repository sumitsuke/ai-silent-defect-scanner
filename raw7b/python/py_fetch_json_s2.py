import requests

def fetch_json(url):
    try:
        # Send a GET request to the specified URL
        response = requests.get(url)
        # Check if the request was successful (HTTP status code 200)
        if response.status_code == 200:
            # Parse the JSON content from the response and return it
            return response.json()
        else:
            # If the request failed, raise an exception with a descriptive message
            raise Exception(f"Failed to fetch JSON. Status code: {response.status_code}")
    except requests.RequestException as e:
        # Handle any exceptions that occur during the HTTP request
        print(f"Error fetching JSON: {e}")
        return None

# Example usage
url = 'https://api.example.com/data'
json_data = fetch_json(url)
if json_data is not None:
    print(json_data)
