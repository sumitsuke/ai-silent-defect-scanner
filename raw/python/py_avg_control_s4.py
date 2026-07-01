def average(numbers):
    # Calculate the sum of all numbers in the list
    total_sum = sum(numbers)
    
    # Check if the list is empty to avoid division by zero error
    if len(numbers) == 0:
        return None
    
    # Calculate the arithmetic mean
    mean = total_sum / len(numbers)
    
    return mean
