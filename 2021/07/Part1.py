#!/usr/bin/env python3

#Advent of Code
#2021 Day 7, Part 1
#Solution by James C. (https://github.com/JamesMCo)

import os, sys
sys.path.append(os.path.abspath("../.."))
import unittest, util.read
from util.tests import run

def solve(puzzle_input):
    bounds = (min(puzzle_input), max(puzzle_input) + 1)
    costs = []

    for candidate in range(*bounds):
        total = 0
        for crab in puzzle_input:
            total += abs(crab - candidate)
        costs.append(total)

    return min(costs)

def main():
    puzzle_input = util.read.as_int_list(",")

    fuel = solve(puzzle_input)

    print("The amount of fuel that must be spent to align the crabs is " + str(fuel) + ".")

class AOC_Tests(unittest.TestCase):
    def test_ex1(self):
        return self.assertEqual(solve([16, 1, 2, 0, 4, 2, 7, 1, 2, 14]), 37)

run(main)
