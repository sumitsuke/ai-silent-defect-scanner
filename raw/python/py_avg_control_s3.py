def average(numbers):
    if not numbers:  # Check if the list is empty
        return None  # Return None for an empty list
    
    total = sum(numbers)  # Calculate the sum of all numbers in the list
    count = len(numbers)  # Get the number of elements in the list
    mean = total / count  # Compute the arithmetic mean
    
    return mean
