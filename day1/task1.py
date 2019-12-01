with open('input', 'r') as file:
    fuel_needed = sum(int(line) // 3 - 2 for line in file)

print(fuel_needed)
