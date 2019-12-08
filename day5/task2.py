import dataclasses

from typing import Callable, Mapping


@dataclasses.dataclass
class Opcode:
    nargs: int
    fn: Callable


def resolve(param, tape, mode):
    return tape[param] if mode == '0' else param


def add(tape, modes, params):
    assert modes[2] == '0'
    params[0] = resolve(params[0], tape, modes[0])
    params[1] = resolve(params[1], tape, modes[1])
    tape[params[2]] = params[0] + params[1]


def mul(tape, modes, params):
    assert modes[2] == '0'
    params[0] = resolve(params[0], tape, modes[0])
    params[1] = resolve(params[1], tape, modes[1])
    tape[params[2]] = params[0] * params[1]


def input_(tape, modes, params):
    assert modes == '000'
    val = int(input())
    tape[params[0]] = val


def output(tape, modes, params):
    params[0] = resolve(params[0], tape, modes[0])
    print(params[0])


def jumptrue(tape, modes, params):
    params[0] = resolve(params[0], tape, modes[0])
    params[1] = resolve(params[1], tape, modes[1])

    if params[0] != 0:
        return params[1]


def jumpfalse(tape, modes, params):
    params[0] = resolve(params[0], tape, modes[0])
    params[1] = resolve(params[1], tape, modes[1])

    if params[0] == 0:
        return params[1]


def lessthan(tape, modes, params):
    params[0] = resolve(params[0], tape, modes[0])
    params[1] = resolve(params[1], tape, modes[1])

    tape[params[2]] = 1 if params[0] < params[1] else 0


def equals(tape, modes, params):
    params[0] = resolve(params[0], tape, modes[0])
    params[1] = resolve(params[1], tape, modes[1])

    tape[params[2]] = 1 if params[0] == params[1] else 0


with open('input', 'r') as f:
    program = list(map(int, f.readline().strip().split(',')))

opcodes: Mapping[int, Opcode] = {}
opcodes[1] = Opcode(nargs=3, fn=add)
opcodes[2] = Opcode(nargs=3, fn=mul)
opcodes[3] = Opcode(nargs=1, fn=input_)
opcodes[4] = Opcode(nargs=1, fn=output)
opcodes[5] = Opcode(nargs=2, fn=jumptrue)
opcodes[6] = Opcode(nargs=2, fn=jumpfalse)
opcodes[7] = Opcode(nargs=3, fn=lessthan)
opcodes[8] = Opcode(nargs=3, fn=equals)


def parse(program):
    ptr = 0
    while True:
        opcode_with_mode = str(program[ptr]).rjust(5, '0')
        opcode_no = int(opcode_with_mode[-2:])
        modes = opcode_with_mode[:-2][::-1]

        if opcode_no == 99:
            break

        opcode = opcodes[opcode_no]
        params = program[ptr + 1:ptr + opcode.nargs + 1]

        updated_ptr = opcode.fn(program, modes, params)

        if updated_ptr is not None:
            ptr = updated_ptr
        else:
            ptr += opcode.nargs + 1


parse(program)
