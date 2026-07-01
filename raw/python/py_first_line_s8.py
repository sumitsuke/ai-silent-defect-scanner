def read_first_line(path):
    # Open the file in read mode
    with open(path, 'r') as file:
        # Read the first line using readline()
        return file.readline().strip()
