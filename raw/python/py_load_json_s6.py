import json

def load_json_file(path):
    with open(path, 'r') as file:
        return json.load(file)
