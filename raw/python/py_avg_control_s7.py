def average(numbers):
    # Initialize sum to 0 and count to 0
    total_sum = 0
    count = 0
    
    # Iterate through each number in the list
    for num in numbers:
        # Add the current number to the total sum
        total_sum += num
        
        # Increment the count of numbers processed
        count += 1
    
    # Calculate the arithmetic mean
    if count > 0:
        average = total_sum / count
    else:
        average = None
    
    return average
