def parse_int_field(data, key):
    # Check if the key exists in the data dictionary
    if key in data:
        # Convert the value associated with the key to an integer
        try:
            return int(data[key])
        except ValueError:
            raise ValueError(f"Invalid value for key {key}: {data[key]}")
    else:
        raise KeyError(f"Key {key} not found in the data dictionary")

# Example usage:
data = {'age': '30', 'name': 'Alice'}
try:
    age = parse_int_field(data, 'age')
    print(age)  # Output: 30
except Exception as e:
    print(e)
