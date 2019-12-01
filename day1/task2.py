import math

fuel_needed = 0


def calc_single_fuel(mass: int) -> int:
    return max(math.floor(int(mass) / 3) - 2, 0)


def calc_fuel_recursively(mass: int) -> int:
    fuel_needed = 0
    while mass > 0:
        mass = calc_single_fuel(mass)
        fuel_needed += mass
    return fuel_needed


with open('input', 'r') as data:
    for line in data:
        mass = int(line)
        fuel_for_current_mass = calc_single_fuel(line)
        fuel_needed += fuel_for_current_mass
        fuel_needed += calc_fuel_recursively(fuel_for_current_mass)

print(fuel_needed)
