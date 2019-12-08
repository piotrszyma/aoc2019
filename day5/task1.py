import dataclasses

from typing import Callable, Mapping


@dataclasses.dataclass
class Opcode:
    nargs: int
    fn: Callable


def add(tape, modes, left_param, right_param, result_param):
    assert modes[2] == '0'
    left_value = tape[left_param] if modes[0] == '0' else left_param
    right_value = tape[right_param] if modes[1] == '0' else right_param
    tape[result_param] = left_value + right_value


def mul(tape, modes, left_param, right_param, result_param):
    assert modes[2] == '0'
    left_value = tape[left_param] if modes[0] == '0' else left_param
    right_value = tape[right_param] if modes[1] == '0' else right_param
    tape[result_param] = left_value * right_value


def input_(tape, modes, param):
    assert modes == '000'
    val = 1
    tape[param] = val


def output(tape, modes, param):
    if modes[0] == '1':
        print(param)
    else:
        print(tape[param])


with open('input', 'r') as f:
    program = list(map(int, f.readline().strip().split(',')))

opcodes: Mapping[int, Opcode] = {}
opcodes[1] = Opcode(nargs=3, fn=add)
opcodes[2] = Opcode(nargs=3, fn=mul)
opcodes[3] = Opcode(nargs=1, fn=input_)
opcodes[4] = Opcode(nargs=1, fn=output)


def parse(program):
    ptr = 0
    while True:
        opcode_with_mode = str(program[ptr]).rjust(5, '0')
        opcode_no = int(opcode_with_mode[-2:])
        modes = opcode_with_mode[:-2][::-1]

        if opcode_no == 99:
            break

        opcode = opcodes[opcode_no]
        opcode.fn(program, modes, *program[ptr + 1:ptr + opcode.nargs + 1])
        ptr += opcode.nargs + 1


parse(program)
