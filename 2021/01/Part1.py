#!/usr/bin/env python3

#Advent of Code
#2021 Day 1, Part 1
#Solution by James C. (https://github.com/JamesMCo)

import os, sys
sys.path.append(os.path.abspath("../.."))
import unittest, util.read
from util.tests import run

def solve(puzzle_input):
    return sum(map(lambda a: a[0] < a[1], zip(puzzle_input[:-1], puzzle_input[1:])))

def main():
    puzzle_input = util.read.as_int_list("\n")

    larger_measurements = solve(puzzle_input)

    print("The number of larger measurements is " + str(larger_measurements) + ".")

class AOC_Tests(unittest.TestCase):
    def test_ex1(self):
        return self.assertEqual(solve([199,
                                       200,
                                       208,
                                       210,
                                       200,
                                       207,
                                       240,
                                       269,
                                       260,
                                       263]), 7)

run(main)
