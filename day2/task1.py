import operator

with open('input', 'r') as f:
    data = [int(value) for value in f.readline().split(',')]

data[1] = 12
data[2] = 2

program_ptr = 0

while data[program_ptr] != 99:
    op = operator.add if data[program_ptr] == 1 else operator.mul
    left_idx = data[program_ptr + 1]
    right_idx = data[program_ptr + 2]
    result_idx = data[program_ptr + 3]
    data[result_idx] = op(data[left_idx], data[right_idx])
    program_ptr += 4

print(data[0])