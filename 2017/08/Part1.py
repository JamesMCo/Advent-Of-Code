#!/usr/bin/env python3

#Advent of Code
#2017 Day 8, Part 1
#Solution by James C. (https://github.com/JamesMCo)

import os, sys
sys.path.append(os.path.abspath("../.."))
import unittest, util.read
from util.tests import run

def solve(puzzle_input):
    registers = {}

    for instruction in puzzle_input:
        i = instruction.split(" ")
        if i[0] not in registers:
            registers[i[0]] = 0
        if i[4] not in registers:
            registers[i[4]] = 0

        if eval(f"registers['{i[4]}'] {i[5]} {i[6]}"):
            if i[1] == "inc":
                registers[i[0]] += int(i[2])
            elif i[1] == "dec":
                registers[i[0]] -= int(i[2])

    return max(registers.values())

def main():
    puzzle_input = util.read.as_lines()

    max_value = solve(puzzle_input)

    print("The largest value in any register is " + str(max_value) + ".")

class AOC_Tests(unittest.TestCase):
    def test_ex1(self):
        self.assertEqual(solve(["b inc 5 if a > 1",
                                "a inc 1 if b < 5",
                                "c dec -10 if a >= 1",
                                "c inc -20 if c == 10"]), 1)

run(main)
