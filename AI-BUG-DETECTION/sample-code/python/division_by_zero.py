def calculate_average(numbers):
    # Bug: Division by zero when list is empty
    total = sum(numbers)
    return total / len(numbers)

# Example usage
print(calculate_average([10, 20, 30]))
print(calculate_average([])) # Crash
