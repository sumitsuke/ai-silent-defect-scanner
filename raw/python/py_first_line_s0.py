def read_first_line(path):
    """
    Opens a text file at the specified path and returns its first line.

    Parameters:
    - path (str): The path to the text file.

    Returns:
    - str: The first line of the file.
    """
    # Open the file in read mode
    with open(path, 'r') as file:
        # Read the first line using readline()
        first_line = file.readline().strip()  # strip() removes leading/trailing whitespace
    return first_line
