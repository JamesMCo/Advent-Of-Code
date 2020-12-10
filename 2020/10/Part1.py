#!/usr/bin/env python3

#Advent of Code
#2020 Day 10, Part 1
#Solution by James C. (https://github.com/JamesMCo)

import os, sys
sys.path.append(os.path.abspath("../.."))
import unittest, util.read
from util.tests import run

def solve(puzzle_input):
    puzzle_input = [0] + sorted(puzzle_input) + [max(puzzle_input) + 3]

    differences = [b - a for a, b in zip(puzzle_input, puzzle_input[1:])]
    return differences.count(1) * differences.count(3)

def main():
    puzzle_input = util.read.as_int_list("\n")

    jolt_differences = solve(puzzle_input)

    print("The product of the 1-jolt differences and 3-jolt differences is " + str(jolt_differences) + ".")

class AOC_Tests(unittest.TestCase):
    def test_ex1(self):
        return self.assertEqual(solve([16, 10, 15, 5, 1, 11, 7, 19, 6, 12, 4]), 35)

    def test_ex2(self):
        return self.assertEqual(solve([28, 33, 18, 42, 31, 14, 46, 20, 48, 47,
                                       24, 23, 49, 45, 19, 38, 39, 11,  1, 32,
                                       25, 35,  8, 17,  7,  9,  4,  2, 34, 10, 3]), 220)

run(main)
