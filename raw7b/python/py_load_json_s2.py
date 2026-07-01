import json

def load_json_file(path):
    """
    Loads and parses a JSON file from the given path.

    Args:
    path (str): The file path of the JSON file to be read.

    Returns:
    dict: A dictionary containing the data loaded from the JSON file.
    """
    with open(path, 'r') as file:
        return json.load(file)
