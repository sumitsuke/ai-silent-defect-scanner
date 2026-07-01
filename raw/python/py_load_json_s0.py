import json

def load_json_file(path):
    # Open the file in read mode
    with open(path, 'r') as file:
        # Load the JSON data from the file
        data = json.load(file)
    
    return data
