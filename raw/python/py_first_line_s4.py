def read_first_line(path):
    # Open the file in read mode
    with open(path, 'r') as file:
        # Read the first line from the file
        first_line = file.readline()
        return first_line.strip()  # Strip any leading/trailing whitespace
