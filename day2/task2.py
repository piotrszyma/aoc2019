import operator

with open('input', 'r') as f:
    data = [int(value) for value in f.readline().split(',')]


def get_result(first, second):
    test_data = data.copy()
    test_data[1] = first
    test_data[2] = second
    program_ptr = 0

    while test_data[program_ptr] != 99:
        op = operator.add if test_data[program_ptr] == 1 else operator.mul
        left_idx = test_data[program_ptr + 1]
        right_idx = test_data[program_ptr + 2]
        result_idx = test_data[program_ptr + 3]
        test_data[result_idx] = op(test_data[left_idx], test_data[right_idx])
        program_ptr += 4

    return test_data[0]


for first in range(99):
    for second in range(99):
        result = get_result(first, second)
        if result == 19690720:
            print(100 * first + second)
            exit(0)
