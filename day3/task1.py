with open('input', 'r') as f:
    WIRES = [wire.strip().split(',') for wire in f.readlines()]

def manh_dist(p0, p1):
    x0, y0 = p0
    x1, y1 = p1
    return abs(x0 - x1) + abs(y0 - y1)


def expand_instr(instr):
    num = int(instr[1:])
    where = instr[0]

    if where == 'U':
        diff = (1, 0)
    elif where == 'R':
        diff = (0, 1)
    elif where == 'D':
        diff = (-1, 0)
    else:
        diff = (0, -1)

    for _ in range(num):
        yield diff


def points_visited(wire):
    base_point = 0, 0
    for instr in wire:
        expanded = expand_instr(instr)
        for single_instr in expanded:
            x, y = base_point
            x_, y_ = single_instr
            base_point = x + x_, y + y_
            yield base_point

lower_manh = 0
base_point = 0, 0
visited_by_first = set(point for point in points_visited(WIRES[0]))

for point in points_visited(WIRES[1]):
    if point in visited_by_first:
        dist = manh_dist(base_point, point)
        lower_manh = min(dist, lower_manh) if lower_manh != 0 else dist

print(lower_manh)
