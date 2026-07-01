def read_first_line(path):
    # Open the file in read mode
    with open(path, 'r') as file:
        # Read the first line of the file
        return file.readline()
