import json

def load_json_file(path):
    """Reads a JSON file at the specified path and returns the parsed dictionary."""
    
    # Open the file in read mode
    with open(path, 'r') as file:
        # Load JSON data from the file
        data = json.load(file)
        
    return data
