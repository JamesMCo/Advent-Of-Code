#!/usr/bin/env python3

#Advent of Code
#2020 Day 1, Part 2
#Solution by James C. (https://github.com/JamesMCo)

import os, sys
sys.path.append(os.path.abspath("../.."))
import unittest, util.read
from util.tests import run

from itertools import combinations

def solve(puzzle_input):
    for a, b, c in combinations(sorted(puzzle_input), 3):
        if a + b + c == 2020:
            return a * b * c

def main():
    puzzle_input = util.read.as_int_list("\n")

    product = solve(puzzle_input)

    print("The product of the three entries that sum to 2020 is " + str(product) + ".")

class AOC_Tests(unittest.TestCase):
    def test_ex1(self):
        return self.assertEqual(solve([1721, 979, 366, 299, 675, 1456]), 241861950)

if __name__ == "__main__":
    run(main)
