import json

def load_json_file(path):
    try:
        with open(path, 'r', encoding='utf-8') as file:
            data = json.load(file)
        return data
    except FileNotFoundError:
        print(f"File not found: {path}")
        return None
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
        return None

# Example usage
file_path = 'example.json'
json_data = load_json_file(file_path)
if json_data is not None:
    print(json.dumps(json_data, indent=4))
