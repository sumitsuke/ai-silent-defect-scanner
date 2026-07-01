def average(numbers):
    if not numbers:
        return 0  # Return 0 for an empty list to avoid division by zero
    
    total = sum(numbers)
    count = len(numbers)
    average_value = total / count
    
    return average_value
