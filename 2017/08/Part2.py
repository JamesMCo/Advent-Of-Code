#!/usr/bin/env python3

#Advent of Code
#Day 8, Part 2
#Solution by James C. (https://github.com/JamesMCo)

import os, sys
sys.path.append(os.path.abspath("../.."))
import unittest
from util.tests import run

def solve(puzzle_input):
    registers = {}
    highest = 0

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
            if registers[i[0]] > highest:
                highest = registers[i[0]]

    return highest

def main():
    f = open("puzzle_input.txt")
    puzzle_input = f.read()[:-1].split("\n")
    f.close()

    highest_value = solve(puzzle_input)

    print("The highes value in any register during this process was " + str(highest_value) + ".")

class AOC_Tests(unittest.TestCase):
    def test_ex1(self):
        self.assertEqual(solve(["b inc 5 if a > 1",
                                "a inc 1 if b < 5",
                                "c dec -10 if a >= 1",
                                "c inc -20 if c == 10"]), 10)

run(main)
