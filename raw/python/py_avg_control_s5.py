def average(numbers):
    if not numbers:  # Check if the list is empty
        return 0  # Return 0 for an empty list
    total_sum = sum(numbers)  # Calculate the sum of all elements in the list
    count = len(numbers)  # Determine the number of elements in the list
    average = total_sum / count  # Calculate the arithmetic mean
    return average  # Return the calculated average
