#!/usr/bin/env python3

#Advent of Code
#2024 Day 17, Part 1
#Solution by James C. (https://github.com/JamesMCo)

import os, sys
sys.path.append(os.path.abspath("../.."))
import unittest, util.read
from util.tests import run

from enum import auto, Enum
import re
from typing import NoReturn, Optional, override, Self
from util.colour import *

def solve(puzzle_input: list[str]) -> str:
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
            self.register_a = a_value
            self.register_b = b_value
            self.register_c = c_value
            return self

        def load_memory(self: Self, data: list[int]) -> Self:
            self.memory = data
            self.debug_log_ip_len = len(str(len(self.memory)))
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

    a: int = int(re.match(r"Register A: (\d+)", puzzle_input[0]).group(1))
    b: int = int(re.match(r"Register B: (\d+)", puzzle_input[1]).group(1))
    c: int = int(re.match(r"Register C: (\d+)", puzzle_input[2]).group(1))
    program: list[int] = [int(n) for n in re.match(r"Program: (\d+(?:,\d+)*)", puzzle_input[4]).group(1).split(",")]

    return ",".join(
        map(
            str,
            Computer()
                .load_registers(a, b, c)
                .load_memory(program)
                .run()
                .outputs
        )
    )

def main() -> tuple[str, str]:
    puzzle_input = util.read.as_lines()

    return "The output of the program is {}.", solve(puzzle_input)

class AOC_Tests(unittest.TestCase):
    def test_ex1(self):
        return self.assertEqual(solve(["Register A: 729",
                                       "Register B: 0",
                                       "Register C: 0",
                                       "",
                                       "Program: 0,1,5,4,3,0"]), "4,6,3,5,6,3,5,2,1,0")

if __name__ == "__main__":
    run(main)
