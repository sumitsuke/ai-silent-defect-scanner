def read_first_line(path):
    # Open the text file in read mode
    with open(path, 'r') as file:
        # Read the first line of the file
        first_line = file.readline()
        return first_line.strip()  # Return the first line after stripping any leading/trailing whitespace
