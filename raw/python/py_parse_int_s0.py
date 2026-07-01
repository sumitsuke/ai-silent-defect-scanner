def parse_int_field(data, key):
    """
    This function takes a dictionary 'data' and a string 'key' as input.
    It attempts to retrieve the value associated with the specified key in the dictionary.
    If the value is found and can be converted to an integer, it returns that integer.
    If the value cannot be converted to an integer or if the key does not exist, it raises a ValueError.

    :param data: Dictionary containing the key-value pairs
    :param key: The key whose value needs to be parsed as an integer
    :return: The integer value associated with the key
    :raises ValueError: If the key does not exist or the value cannot be converted to an integer
    """
    if key in data:
        try:
            return int(data[key])
        except ValueError:
            raise ValueError(f"Cannot convert value of {data[key]} for key {key} to an integer")
    else:
        raise KeyError(f"Key {key} does not exist in the dictionary")

# Example usage
data = {'name': 'John', 'age': '30'}
try:
    print(parse_int_field(data, 'age'))  # Output: 30
except ValueError as e:
    print(e)

try:
    print(parse_int_field(data, 'gender'))  # Raises KeyError
except ValueError as e:
    print(e)
