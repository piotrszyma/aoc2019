import math

fuel_needed = 0

with open('input', 'r') as data:
    for line in data:
        fuel_needed += math.floor(int(line) / 3) - 2

print(fuel_needed)
