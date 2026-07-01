import json

def load_json_file(path):
    """
    Loads the JSON file at the specified path and returns the parsed dictionary.

    Parameters:
    - path (str): The path to the JSON file.

    Returns:
    - dict: The parsed dictionary from the JSON file.
    """
    with open(path, 'r') as file:
        data = json.load(file)
    return data
