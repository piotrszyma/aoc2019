import collections

orbited_by = collections.defaultdict(set)

with open('input', 'r') as f:
    for line in (l.strip() for l in f):
        planet, orbit = line.split(')')
        orbited_by[planet].add(orbit)
        assert orbited_by[orbit] is not None


def no_orbits(place):
    return len(orbited_by[place]) + sum(
        no_orbits(orbit) for orbit in orbited_by[place])


def no_of_all_orbits(places):
    return sum(no_orbits(place) for place in places)


print(no_of_all_orbits(orbited_by.keys()))
