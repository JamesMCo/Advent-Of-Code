#!/usr/bin/env python3

#Advent of Code
#2016 Day 12, Part 1
#Solution by James C. (https://github.com/JamesMCo)

import os, sys
sys.path.append(os.path.abspath("../.."))
import unittest, util.read
from util.tests import run

def solve(puzzle_input):
    registers = {}

    i = 0
    while i < len(puzzle_input):
        j = puzzle_input[i].split(" ")
        if j[0] == "cpy":
            try:
                int(j[1])
                registers[j[2]] = int(j[1])
            except:
                registers[j[2]] = registers[j[1]]
        elif j[0] == "inc":
            registers[j[1]] += 1
        elif j[0] == "dec":
            registers[j[1]] -= 1
        elif j[0] == "jnz":
            try:
                int(j[1])
                if j[1] != "0":
                    i += int(j[2]) - 1
            except:
                if j[1] in registers and registers[j[1]] != 0 and j[2] != 0:
                    i += int(j[2]) - 1
        i += 1

    return registers["a"]

def main():
    puzzle_input = util.read.as_lines()

    register_a = solve(puzzle_input)

    print("The value of register a is " + str(register_a) + ".")

class AOC_Tests(unittest.TestCase):
    def test_ex1(self):
        self.assertEqual(solve(["cpy 41 a",
                                "inc a",
                                "inc a",
                                "dec a",
                                "jnz a 2",
                                "dec a"]), 42)

run(main)
