def read_first_line(path):
    """
    Open the text file at 'path' and return its first line.

    Args:
    path (str): The path to the text file.

    Returns:
    str: The first line of the file.
    """
    with open(path, 'r') as file:
        return file.readline().strip()
