#!/usr/bin/env python3

#Advent of Code
#2019 Day 7, Part 1
#Solution by James C. (https://github.com/JamesMCo)

import os, sys
sys.path.append(os.path.abspath("../.."))
import unittest, util.read
from util.tests import run

from itertools import permutations
from util.intcode_2019 import IntcodeComputer

def solve(puzzle_input):
    amp = IntcodeComputer().load_memory(puzzle_input)

    def try_sequence(seq):
        prev_output = 0
        for phase in seq:
            prev_output = amp.reset().queue_inputs([phase, prev_output]).run().outputs[-1]
        return prev_output

    return max(try_sequence(x) for x in permutations([0, 1, 2, 3, 4]))

def main():
    puzzle_input = util.read.as_int_list(",")

    signal = solve(puzzle_input)

    print("The highest signal that can be sent to the thrusters is " + str(signal) + ".")

class AOC_Tests(unittest.TestCase):
    def test_ex1(self):
        self.assertEqual(solve([3, 15, 3, 16, 1002, 16, 10, 16, 1, 16, 15, 15, 4, 15 , 99, 0, 0]), 43210)

    def test_ex2(self):
        self.assertEqual(solve([3,   23,  3, 24, 1002, 24, 10, 24, 1002, 23, -1, 23,
                                101,  5, 23, 23,    1, 24, 23, 23,    4, 23, 99,  0, 0]), 54321)

    def test_ex3(self):
        self.assertEqual(solve([3,    31, 3, 32, 1002, 32, 10, 32, 1001, 31, -2, 31, 1007, 31,  0, 33,
                                1002, 33, 7, 33,    1, 33, 31, 31,    1, 32, 31, 31,    4, 31, 99,  0, 0, 0]), 65210)

run(main)
