#!/usr/bin/env python3

#Advent of Code
#2024 Day 17, Part 2
#Solution by James C. (https://github.com/JamesMCo)

import os, sys
sys.path.append(os.path.abspath("../.."))
import unittest, util.read
from util.tests import run

from enum import auto, Enum
from itertools import zip_longest
import re
from typing import Iterable, NoReturn, Optional, override, Self
from util.colour import *

def solve(puzzle_input: list[str], actual_input: bool = True) -> int:
    # Overall computer implementation based heavily
    # on my 2019 IntCode Computer implementation
    # (because I really like it)
    # https://github.com/JamesMCo/Advent-Of-Code/blob/master/util/intcode_2019.py

    class OperandType(Enum):
        UNDEFINED = auto()
        LITERAL   = auto()
        COMBO     = auto()

    class Instruction:
        name: str   = ""
        opcode: int = -1
        operand_type: OperandType = OperandType.UNDEFINED

        computer: "Computer"
        operand: int

        def __init__(self: Self, computer: "Computer", memory_address: int) -> None:
            self.computer = computer
            self.operand = self.computer.peek_memory(memory_address + 1)

        def get_operand(self: Self) -> int:
            match self.operand_type, self.operand:
                case OperandType.UNDEFINED, _:         raise RuntimeError("Operator does not define operand type")
                case OperandType.LITERAL, _:           return self.operand
                case OperandType.COMBO, 0 | 1 | 2 | 3: return self.operand
                case OperandType.COMBO, 4:             return self.computer.register_a
                case OperandType.COMBO, 5:             return self.computer.register_b
                case OperandType.COMBO, 6:             return self.computer.register_c
                case OperandType.COMBO, 7:             raise RuntimeError("Combo operand 7 is reserved")

        def run(self: Self) -> None:
            raise NotImplementedError()

        def __str__(self: Self) -> str:
            return f"{yellow(self.name)} {bright_green(f"operand={self.operand}")} {green("(" + self.operand_type.name + ")")}"

        _instructions: Optional[dict[int, Self]] = None
        @classmethod
        def get(cls: Self, computer: "Computer", memory_address: int) -> Self | NoReturn:
            if cls._instructions is None:
                cls._instructions = {inst.opcode: inst for inst in cls.__subclasses__()}

            opcode: int = computer.peek_memory(memory_address)
            return cls._instructions[opcode](computer, memory_address)

    class ADV(Instruction):
        name:   str = "ADV"
        opcode: int = 0
        operand_type: OperandType = OperandType.COMBO

        @override
        def run(self: Self) -> None:
            self.computer.register_a = int(self.computer.register_a / (2 ** self.get_operand()))

    class BXL(Instruction):
        name:   str = "BXL"
        opcode: int = 1
        operand_type: OperandType = OperandType.LITERAL

        @override
        def run(self: Self) -> None:
            self.computer.register_b ^= self.get_operand()

    class BST(Instruction):
        name:   str = "BST"
        opcode: int = 2
        operand_type: OperandType = OperandType.COMBO

        @override
        def run(self: Self) -> None:
            self.computer.register_b = self.get_operand() % 8

    class JNZ(Instruction):
        name:   str = "JNZ"
        opcode: int = 3
        operand_type: OperandType = OperandType.LITERAL

        @override
        def run(self: Self) -> None:
            if self.computer.register_a != 0:
                self.computer.init_ip(self.get_operand())

    class BXC(Instruction):
        name:   str = "BXC"
        opcode: int = 4
        operand_type: OperandType = OperandType.UNDEFINED

        @override
        def run(self: Self) -> None:
            self.computer.register_b ^= self.computer.register_c

    class OUT(Instruction):
        name:   str = "OUT"
        opcode: int = 5
        operand_type: OperandType = OperandType.COMBO

        @override
        def run(self: Self) -> None:
            self.computer.output(self.get_operand() % 8)

    class BDV(Instruction):
        name:   str = "BDV"
        opcode: int = 6
        operand_type: OperandType = OperandType.COMBO

        @override
        def run(self: Self) -> None:
            self.computer.register_b = int(self.computer.register_a / (2 ** self.get_operand()))

    class CDV(Instruction):
        name:   str = "CDV"
        opcode: int = 7
        operand_type: OperandType = OperandType.COMBO

        @override
        def run(self: Self) -> None:
            self.computer.register_c = int(self.computer.register_a / (2 ** self.get_operand()))

    class Computer:
        debug_log: bool
        debug_log_ip_len: int
        memory: list[int]
        initial_register_a: int
        initial_register_b: int
        initial_register_c: int
        register_a: int
        register_b: int
        register_c: int
        instruction_pointer: int
        outputs: list[int]
        halted: bool

        def __init__(self: Self, debug_log: bool = False) -> None:
            self.debug_log = debug_log
            self.debug_log_ip_len = 1
            self.register_a = 0
            self.register_b = 0
            self.register_c = 0
            self.init_ip()
            self.outputs = []
            self.halted = False

        def init_ip(self: Self, address: int = 0) -> Self:
            self.instruction_pointer = address
            return self

        def load_registers(self: Self, a_value: int, b_value: int, c_value: int) -> Self:
            self.initial_register_a = a_value
            self.initial_register_b = b_value
            self.initial_register_c = c_value
            self.register_a = a_value
            self.register_b = b_value
            self.register_c = c_value
            return self

        def load_memory(self: Self, data: list[int]) -> Self:
            self.memory = data
            self.debug_log_ip_len = len(str(len(self.memory)))
            return self

        def reset(self: Self) -> Self:
            self.register_a = self.initial_register_a
            self.register_b = self.initial_register_b
            self.register_c = self.initial_register_c
            self.init_ip()
            self.outputs.clear()
            self.halted = False
            return self

        def peek_memory(self: Self, address: int) -> int | NoReturn:
            if address < 0 or address >= len(self.memory):
                raise IndexError(f"Address {address} out of memory")
            return self.memory[address]

        def output(self: Self, value: int) -> None:
            self.outputs.append(value)

            if self.debug_log:
                print(f"[{red(f"{"OUT": >{self.debug_log_ip_len}}")}] {blue(value)}")

        def step(self: Self) -> bool:
            if self.instruction_pointer < 0 or self.instruction_pointer >= len(self.memory):
                self.halted = True

            if not self.halted:
                current_instruction: Instruction = Instruction.get(self, self.instruction_pointer)

                if self.debug_log:
                    print(f"[{cyan(f"{self.instruction_pointer: >{self.debug_log_ip_len}}")}] {current_instruction}")

                before_instruction_pointer: int = self.instruction_pointer
                current_instruction.run()
                if before_instruction_pointer == self.instruction_pointer:
                    # Instruction pointer was not modified (i.e. by jumping)
                    self.instruction_pointer += 2

            return not self.halted

        def run(self: Self) -> Self:
            while not self.halted:
                self.step()
            return self

        def run_and_yield_outputs(self: Self) -> Iterable[int]:
            while not self.halted:
                self.step()
                if self.outputs:
                    yield self.outputs[0]
                    self.outputs.clear()

    a: int = 0
    b: int = int(re.match(r"Register B: (\d+)", puzzle_input[1]).group(1))
    c: int = int(re.match(r"Register C: (\d+)", puzzle_input[2]).group(1))
    program: list[int] = [int(n) for n in re.match(r"Program: (\d+(?:,\d+)*)", puzzle_input[4]).group(1).split(",")]

    if not actual_input:
        device: Computer = Computer(False).load_memory(program)
        while True:
            a += 1
            device.load_registers(a, b, c)
            if all(original == output for original, output in zip_longest(program, device.run_and_yield_outputs())):
                return a
            device.reset()
    else:
        # Algorithm to generate a value of A from my puzzle input - NOT a generic solution
        # 2,4 - BST 4
        # 1,3 - BXL 3
        # 7,5 - CDV 5
        # 0,3 - ADV 3
        # 1,5 - BXL 5
        # 4,1 - BXC 1
        # 5,5 - OUT 5
        # 3,0 - JNZ 0
        #
        # The program takes chunks of the initial value of A three bits at a time, starting
        # at the least significant digits and working to the most significant digits, stopping
        # when none of the bits are set.
        #
        # An intermediate value is calculated from the chunk by flipping the two least significant bits.
        #
        # The output value is the intermediate value XORed with 5, then XORed with the three bits after
        # shifting by the intermediate value.
        #
        # The A value is then right shifted 3 bits to prepare for the next iteration.

        def run_a(initial_a: int) -> Iterable[int]:
            register_a = initial_a
            while register_a != 0:
                yield (register_a ^ 6 ^ (register_a >> ((register_a % 8) ^ 3))) % 8
                register_a = register_a >> 3

        def test_a(initial_a: int, expected_output: list[int]) -> bool:
            return all(original == output for original, output in zip_longest(expected_output, run_a(initial_a)))

        def generate_a(remaining_numbers: list[int]) -> Iterable[int]:
            # Generate all values of A that will give the remaining numbers as output
            # Do so by recursing (taking the head off the list each time)
            # Base case is no remaining numbers, in which case try every 3-bit value (i.e. 0-8)

            if not remaining_numbers:
                for bits in range(0, 8):
                    yield bits
                    input()
                return
            for future_bits in generate_a(remaining_numbers[1:]):
                for current_a in range(0, 8):
                    test_bits: int = (future_bits << 3) | current_a
                    if test_a(test_bits, remaining_numbers):
                        yield test_bits

        generated_a: int = next(a for a in generate_a(program))

        # Uncomment to verify that the generated value of A is valid before returning it
        # if all(original == output for original, output in zip_longest(program, run_a(generated_a))):
        #     return generated_a
        # else:
        #     raise RuntimeError(f"Unable to validate generated A, {generated_a}, as being correct")

        return generated_a

def main() -> tuple[str, int]:
    puzzle_input = util.read.as_lines()

    return "The lowest positive initial value for register A that causes the program to output a copy of itself is {}.", solve(puzzle_input)

class AOC_Tests(unittest.TestCase):
    def test_ex1(self):
        return self.assertEqual(solve(["Register A: 2024",
                                       "Register B: 0",
                                       "Register C: 0",
                                       "",
                                       "Program: 0,3,5,4,3,0"], False), 117440)

if __name__ == "__main__":
    run(main)
