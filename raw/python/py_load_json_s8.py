import json

def load_json_file(path):
    """
    Reads a JSON file at the specified path and returns the parsed dictionary.

    Args:
    path (str): The path to the JSON file.

    Returns:
    dict: The parsed JSON data as a dictionary.
    """
    try:
        with open(path, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"File not found at {path}")
        return None
    except json.JSONDecodeError as e:
        print(f"Failed to decode JSON file: {e}")
        return None

# Example usage
json_data = load_json_file('example.json')
if json_data is not None:
    print(json_data)
