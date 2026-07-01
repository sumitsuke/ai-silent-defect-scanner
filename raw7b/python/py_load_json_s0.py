import json

def load_json_file(path):
    """
    Read a JSON file from the specified path and return the parsed dictionary.

    Args:
    path (str): The file path to the JSON file to be read.

    Returns:
    dict: The dictionary containing the data parsed from the JSON file.
    """
    with open(path, 'r') as file:
        data = json.load(file)
    return data
