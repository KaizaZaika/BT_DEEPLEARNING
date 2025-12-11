def calculate_average(numbers):
    total = 0
    # Error: Range is short by 1
    for i in range(len(numbers) - 1):
        total += numbers[i]
    
    # Error: No check for empty list (div by zero)
    average = total / len(numbers)
    
    # Error: Prints instead of returns
    print(average)

data = [] 
calculate_average(data)
