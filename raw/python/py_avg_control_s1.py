def average(numbers):
    if not numbers:
        return None  # Return None if the list is empty
    
    total = sum(numbers)
    count = len(numbers)
    return total / count
