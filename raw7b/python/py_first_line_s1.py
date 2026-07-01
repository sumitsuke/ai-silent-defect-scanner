def read_first_line(path):
    """
    Reads and returns the first line of the text file at the given path.

    Args:
    path (str): The path to the text file.

    Returns:
    str: The first line of the file, or an empty string if the file is empty or does not exist.
    
    Raises:
    FileNotFoundError: If the file does not exist at the specified path.
    IOError: If an error occurs while reading the file.
    """
    try:
        with open(path, 'r') as file:
            first_line = file.readline().strip()  # Read the first line and strip any leading/trailing whitespace
            return first_line
    except FileNotFoundError:
        print(f"File not found: {path}")
        raise
    except IOError as e:
        print(f"An error occurred while reading the file: {e}")
        raise

# Example usage:
# try:
#     first_line = read_first_line('example.txt')
#     print(f"The first line of the file is: '{first_line}'")
# except Exception as e:
#     print(e)
