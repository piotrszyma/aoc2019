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

layers = [group for group in grouper(data, LAYER_SIZE)]


def get_result_image(layers):
    for idx, _ in enumerate(layers[0]):
        for layer in layers:
            if layer[idx] != '2':
                yield layer[idx]
                found = True
                break


final_image = '\n'.join(''.join('#' if e == '1' else ' ' for e in group)
                        for group in grouper(get_result_image(layers), WIDTH))

print(final_image)  # Check stdout for result.
