def parse_int_field(data, key):
    try:
        return int(data[key])
    except (KeyError, ValueError) as e:
        print(f"Error parsing field '{key}': {e}")
        return None
