#!/usr/bin/env python3

#Advent of Code
#2019 Day 9, Part 1
#Solution by James C. (https://github.com/JamesMCo)

import os, sys
sys.path.append(os.path.abspath("../.."))
import unittest, util.read
from util.tests import run

from util.intcode_2019 import IntcodeComputer

def solve(puzzle_input):
    return IntcodeComputer().load_memory(puzzle_input).queue_inputs(1).run().outputs

def main():
    puzzle_input = util.read.as_int_list(",")

    keycode = solve(puzzle_input)[-1]

    print("The BOOST keycode the computer produces is " + str(keycode) + ".")

class AOC_Tests(unittest.TestCase):
    def test_ex1(self):
        self.assertEqual(solve([109, 1, 204, -1, 1001, 100, 1, 100, 1008, 100, 16, 101, 1006, 101, 0, 99]),
                               [109, 1, 204, -1, 1001, 100, 1, 100, 1008, 100, 16, 101, 1006, 101, 0, 99])

    def test_ex2(self):
        self.assertEqual(len(str(solve([1102,34915192,34915192,7,4,7,99, 0])[0])), 16)

    def test_ex3(self):
        self.assertEqual(solve([104, 1125899906842624, 99])[0], 1125899906842624)

if __name__ == "__main__":
    run(main)
