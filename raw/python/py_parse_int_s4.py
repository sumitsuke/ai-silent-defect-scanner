def parse_int_field(data, key):
    # Check if the key exists in the dictionary
    if key in data:
        # Attempt to convert the value associated with the key to an integer
        try:
            return int(data[key])
        except ValueError:
            # If conversion fails, raise a ValueError indicating invalid data type
            raise ValueError(f"Invalid data type for key {key}: expected integer")
    else:
        # If the key does not exist in the dictionary, raise a KeyError
        raise KeyError(f"Key {key} does not exist in the dictionary")

# Example usage
data = {'age': '30'}
try:
    age = parse_int_field(data, 'age')
    print(age)  # Output: 30
except ValueError as e:
    print(e)

try:
    age = parse_int_field(data, 'height')  # This will raise a KeyError
    print(age)
except ValueError as e:
    print(e)
