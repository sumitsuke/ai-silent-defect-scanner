import requests

def fetch_json(url):
    try:
        # Perform an HTTP GET request to the specified URL
        response = requests.get(url)
        
        # Raise an exception if the request was unsuccessful
        response.raise_for_status()
        
        # Parse the JSON body of the response and return it as a dictionary
        json_data = response.json()
        return json_data
    
    except requests.exceptions.RequestException as e:
        # Handle any exceptions that may occur during the request
        print(f"An error occurred: {e}")
        return None

# Example usage:
# url = "https://api.example.com/data"
# data = fetch_json(url)
# if data is not None:
#     print(data)
