#!/usr/bin/env python3

#Advent of Code
#2019 Day 21, Part 1
#Solution by James C. (https://github.com/JamesMCo)

import os, sys
sys.path.append(os.path.abspath("../.."))
import unittest, util.read
from util.tests import run

import typing as t
from util.colour import bright_green, yellow
from util.intcode_2019 import IntcodeComputer

def solve(puzzle_input):
    class Register:
        name: str

        def __init__(self: t.Self, name: str) -> None:
            self.name = name

        def __str__(self: t.Self) -> str:
            return bright_green(self.name)

    A, B, C, D, J, T = [Register(name) for name in "ABCDJT"]

    class Instruction:
        name: str
        parameters: list[Register]

        def __init__(self: t.Self, name: str, parameters: list[Register]) -> None:
            self.name = name
            self.parameters = parameters

        def __str__(self: t.Self) -> str:
            return " ".join([yellow(self.name), *map(str, self.parameters)])

        def raw_str(self: t.Self) -> str:
            return " ".join([self.name, *[param.name for param in self.parameters]])

    def AND(x: Register, y: Register) -> Instruction:
        return Instruction("AND", [x, y])

    def OR(x: Register, y: Register) -> Instruction:
        return Instruction("OR", [x, y])

    def NOT(x: Register, y: Register) -> Instruction:
        return Instruction("NOT", [x, y])

    class SpringScript:
        computer: IntcodeComputer
        script: list[Instruction]

        def __init__(self: t.Self, print_output: bool = False) -> None:
            self.computer = IntcodeComputer().load_memory(puzzle_input)
            if print_output:
                self.computer.register_output_listener(self.output)

        @staticmethod
        def output(value: int):
            try:
                print(chr(value), end="")
            except ValueError:
                # Not a printable character
                pass

        def load_script(self: t.Self, script: list[Instruction]) -> t.Self:
            self.script = script
            return self

        def run(self: t.Self) -> int:
            self.computer.reset()\
                .queue_inputs("\n".join(map(Instruction.raw_str, self.script)) + "\n")\
                .queue_inputs("WALK\n")\
                .run()
            return self.computer.outputs[-1]

    return SpringScript().load_script([
        # If any of A, B, or C are a hole, and D is not a hole, then jump
        NOT(A, J),
        NOT(B, T),
        OR(T, J),
        NOT(C, T),
        OR(T, J),
        AND(D, J)
    ]).run()

def main():
    puzzle_input = util.read.as_int_list(",")

    hull_damage = solve(puzzle_input)

    print("The amount of hull damage reported is " + str(hull_damage) + ".")

class AOC_Tests(unittest.TestCase):
    @unittest.skip("No test cases")
    def test_ex1(self):
        pass

if __name__ == "__main__":
    run(main)
