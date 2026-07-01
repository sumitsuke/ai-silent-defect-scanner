def average(numbers):
    if not numbers:
        return 0  # Return 0 if the list is empty
    return sum(numbers) / len(numbers)
