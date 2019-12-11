import dataclasses
import itertools
import collections
import operator
from pprint import pprint

from typing import Callable, Mapping, Sequence, Optional


class Status:
    REQUIRE_INPUT = 'REQUIRE_INPUT'
    HAS_OUTPUT = 'HAS_OUTPUT'
    DONE = 'DONE'
    WORKING = 'WORKING'
    NOT_RUN = 'NOT_RUN'


@dataclasses.dataclass
class Opcode:
    nargs: int
    fn: Callable
    pre: Optional[Status] = None
    post: Optional[Status] = None


class Machine:
    def __init__(self, tape: Sequence[int]):
        opcodes: Mapping[int, Opcode] = {}
        opcodes[1] = Opcode(nargs=3, fn=self.add)
        opcodes[2] = Opcode(nargs=3, fn=self.mul)
        opcodes[3] = Opcode(nargs=1, fn=self.input_, pre=Status.REQUIRE_INPUT)
        opcodes[4] = Opcode(nargs=1, fn=self.output, post=Status.HAS_OUTPUT)
        opcodes[5] = Opcode(nargs=2, fn=self.jumptrue)
        opcodes[6] = Opcode(nargs=2, fn=self.jumpfalse)
        opcodes[7] = Opcode(nargs=3, fn=self.lessthan)
        opcodes[8] = Opcode(nargs=3, fn=self.equals)

        self.input = None
        self.output = None
        self.opcodes = opcodes
        self.tape = tape.copy()
        self.ptr = 0
        self.status = Status.NOT_RUN
        self.iter = None

    def __repr__(self):
        return f'Machine (state: {self.status}, ptr: {self.ptr}, input: "{self.input}", output: "{self.output}")'

    def set_input(self, value):
        if self.status != Status.REQUIRE_INPUT:
            raise RuntimeError(
                "Feeeding input to machine that does not require it.")
        self.input = value
        self.status = Status.WORKING
        next(self.iter)

    def get_output(self):
        if self.status != Status.HAS_OUTPUT:
            raise RuntimeError(
                "Requiring output from machines that does not have one.")

        if self.status == Status.DONE:
            return self.output

        output = self.output
        self.output = None
        self.status = Status.WORKING
        next(self.iter)
        return output

    def start(self):
        self.iter = self.run()
        next(self.iter)

    def run(self):
        while True:
            self.status = Status.WORKING
            opcode_with_mode = str(self.tape[self.ptr]).rjust(5, '0')
            opcode_no = int(opcode_with_mode[-2:])
            modes = opcode_with_mode[:-2][::-1]

            if opcode_no == 99:
                self.status = Status.DONE
                yield
                return

            opcode = self.opcodes[opcode_no]
            params = self.tape[self.ptr + 1:self.ptr + opcode.nargs + 1]

            if opcode.pre:  # input
                self.status = opcode.pre
                yield

            opcode.fn(modes, params, opcode.nargs)

            if opcode.post:
                self.status = opcode.post
                yield

    def resolve(self, param, mode):
        return self.tape[param] if mode == '0' else param

    def add(self, modes, params, nargs):
        assert modes[2] == '0'
        params[0] = self.resolve(params[0], modes[0])
        params[1] = self.resolve(params[1], modes[1])
        self.tape[params[2]] = params[0] + params[1]
        self.ptr += nargs + 1

    def mul(self, modes, params, nargs):
        assert modes[2] == '0'
        params[0] = self.resolve(params[0], modes[0])
        params[1] = self.resolve(params[1], modes[1])
        self.tape[params[2]] = params[0] * params[1]
        self.ptr += nargs + 1

    def input_(self, modes, params, nargs):
        assert modes == '000'
        if self.input is None:
            raise RuntimeError('Executes input, but one not provided.')
        self.tape[params[0]] = self.input
        self.ptr += nargs + 1
        self.input = None

    def output(self, modes, params, nargs):
        params[0] = self.resolve(params[0], modes[0])
        self.ptr += nargs + 1
        if self.output:
            raise RuntimeError('Executes output, but has uncollected output.')
        self.output = params[0]  # TODO: fix it

    def jumptrue(self, modes, params, nargs):
        params[0] = self.resolve(params[0], modes[0])
        params[1] = self.resolve(params[1], modes[1])

        if params[0] != 0:
            self.ptr = params[1]
        else:
            self.ptr += nargs + 1

    def jumpfalse(self, modes, params, nargs):
        params[0] = self.resolve(params[0], modes[0])
        params[1] = self.resolve(params[1], modes[1])

        if params[0] == 0:
            self.ptr = params[1]
        else:
            self.ptr += nargs + 1

    def lessthan(self, modes, params, nargs):
        params[0] = self.resolve(params[0], modes[0])
        params[1] = self.resolve(params[1], modes[1])

        self.tape[params[2]] = 1 if params[0] < params[1] else 0
        self.ptr += nargs + 1

    def equals(self, modes, params, nargs):
        params[0] = self.resolve(params[0], modes[0])
        params[1] = self.resolve(params[1], modes[1])

        self.tape[params[2]] = 1 if params[0] == params[1] else 0
        self.ptr += nargs + 1


with open('input', 'r') as f:
    program = list(map(int, f.readline().strip().split(',')))


def try_perm(combination):
    previous_output = 0

    machines = [
        Machine(program),
        Machine(program),
        Machine(program),
        Machine(program),
        Machine(program),
    ]

    for machine in machines:
        machine.start()

    for machine, init_state in zip(machines, combination):
        machine.set_input(init_state)

    while True:
        for machine in machines:
            machine.set_input(previous_output)
            previous_output = machine.get_output()

        if machines[0].status == Status.DONE:
            break

    return previous_output


best = (-1, None)

for perm in itertools.permutations(range(5, 10)):
    current_result = try_perm(perm)
    best = max([current_result, perm], best, key=operator.itemgetter(0))

pprint(best)
