#!/usr/bin/env python3

#Advent of Code
#2019 Day 5, Part 2
#Solution by James C. (https://github.com/JamesMCo)

import os, sys
sys.path.append(os.path.abspath("../.."))
import unittest, util.read
from util.tests import run

from util.intcode_2019 import IntcodeComputer

def solve(puzzle_input):
    return IntcodeComputer().load_memory(puzzle_input).queue_inputs([5]).run().outputs[-1]

def main():
    puzzle_input = util.read.as_int_list(",")

    diag_code = solve(puzzle_input)

    print("The diagnostic code the program produces is " + str(diag_code) + ".")

class AOC_Tests(unittest.TestCase):
    @unittest.skip("No test cases")
    def test_ex1(self):
        pass

run(main)
