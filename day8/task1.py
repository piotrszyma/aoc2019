import itertools
import operator

WIDTH, HEIGHT = 25, 6
LAYER_SIZE = WIDTH * HEIGHT


def grouper(iterable, n, fillvalue=None):
    "Collect data into fixed-length chunks or blocks"
    # grouper('ABCDEFG', 3, 'x') --> ABC DEF Gxx
    args = [iter(iterable)] * n
    return itertools.zip_longest(fillvalue=fillvalue, *args)


with open('input', 'r') as f:
    data = list(f.readline())

best = ['0'] * LAYER_SIZE

for group in grouper(data, LAYER_SIZE):
    best = min(group, best, key=lambda group: group.count('0'))

print(best.count('1') * best.count('2'))
