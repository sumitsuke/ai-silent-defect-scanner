def read_first_line(path):
    try:
        # Open the file in read mode
        with open(path, 'r') as file:
            # Read the first line of the file
            first_line = file.readline()
            return first_line.strip()  # Return the stripped line
    except FileNotFoundError:
        print(f"File not found at {path}")
        return None

# Example usage
file_path = "example.txt"
first_line = read_first_line(file_path)
if first_line is not None:
    print(f"The first line of the file is: {first_line}")
