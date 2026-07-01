import json

def load_json_file(path):
    """
    Read a JSON file and return the parsed dictionary.

    Args:
    path (str): The path to the JSON file.

    Returns:
    dict: The parsed dictionary from the JSON file.
    """
    with open(path, 'r') as file:
        return json.load(file)
