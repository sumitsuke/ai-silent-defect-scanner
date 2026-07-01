def average(numbers):
    """
    Calculate the arithmetic mean of a list of numbers.

    Args:
    numbers (list): A list of numerical values.

    Returns:
    float: The arithmetic mean of the list.
    """
    if not numbers:  # Check if the list is empty
        return 0.0  # Return 0 for an empty list as the mean

    sum_of_numbers = sum(numbers)  # Sum all elements in the list
    count_of_numbers = len(numbers)  # Count the number of elements in the list

    # Calculate the arithmetic mean
    average_result = sum_of_numbers / count_of_numbers

    return average_result
