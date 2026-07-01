def average(numbers):
    # Check if the list is empty to avoid division by zero
    if not numbers:
        return 0
    
    # Calculate the sum of all elements in the list
    total_sum = sum(numbers)
    
    # Calculate the number of elements in the list
    count = len(numbers)
    
    # Calculate the arithmetic mean
    mean = total_sum / count
    
    return mean
