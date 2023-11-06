#!/usr/bin/env python3

#Advent of Code
#2019 Day 2, Part 2
#Solution by James C. (https://github.com/JamesMCo)

import os, sys
sys.path.append(os.path.abspath("../.."))
import unittest, util.read
from util.tests import run

from util.intcode_2019 import IntcodeComputer

def solve(puzzle_input):
    computer = IntcodeComputer()

    for noun in range(0, 100):
        for verb in range(0, 100):
            computer.load_memory(puzzle_input).init_ip()
            computer.memory[1] = noun
            computer.memory[2] = verb

            if computer.run().peek_memory(0) == 19690720:
                return 100 * noun + verb

def main():
    puzzle_input = util.read.as_int_list(",")

    value = solve(puzzle_input)

    print("The value of 100 * noun + verb is " + str(value) + ".")

class AOC_Tests(unittest.TestCase):
    @unittest.skip("No test cases")
    def test_ex1(self):
        pass

run(main)
