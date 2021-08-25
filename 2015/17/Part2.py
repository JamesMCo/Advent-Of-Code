#!/usr/bin/env python3

#Advent of Code
#2015 Day 17, Part 2
#Solution by James C. (https://github.com/JamesMCo)

import os, sys
sys.path.append(os.path.abspath("../.."))
import unittest, util.read
from util.tests import run
from itertools import combinations

def solve(puzzle_input, target=150):
    seen = 0
    minimum = len(puzzle_input)+1

    for i in range(1, len(puzzle_input)+1):
        for arr in combinations(puzzle_input, i):
            if sum(arr) == target:
                if len(arr) == minimum:
                    seen += 1
                elif len(arr) < minimum:
                    minimum = len(arr)
                    seen = 1

    return seen

def main():
    puzzle_input = util.read.as_int_list("\n")

    ways = solve(puzzle_input)

    print("The number of different ways to fill the minimum number of containers that can fit 150 litres of eggnog is " + str(ways) + ".")

class AOC_Tests(unittest.TestCase):
    def test_ex1(self):
        return self.assertEqual(solve([20, 15, 10, 5, 5], 25), 3)

run(main)
