def read_first_line(path):
    """
    Open a text file at the specified path and return its first line.
    
    Parameters:
    - path: str, the path to the text file
    
    Returns:
    - str, the first line of the text file
    """
    with open(path, 'r') as file:
        return file.readline()
