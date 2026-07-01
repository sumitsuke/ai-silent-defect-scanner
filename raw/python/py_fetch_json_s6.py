import requests

def fetch_json(url):
    response = requests.get(url)
    if response.status_code == 200:
        try:
            return response.json()
        except ValueError:
            print(f"Error parsing JSON: {response.text}")
            return None
    else:
        print(f"Failed to retrieve data from {url}. Status code: {response.status_code}")
        return None
