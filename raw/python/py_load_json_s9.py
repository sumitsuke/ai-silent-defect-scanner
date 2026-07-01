import json

def load_json_file(path):
    """
    Load a JSON file from the given path and return the parsed dictionary.

    Args:
    path (str): The path to the JSON file.

    Returns:
    dict: A dictionary containing the data read from the JSON file.
    """
    with open(path, 'r', encoding='utf-8') as file:
        return json.load(file)
