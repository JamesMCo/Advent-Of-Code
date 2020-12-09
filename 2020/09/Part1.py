#!/usr/bin/env python3

#Advent of Code
#2020 Day 9, Part 1
#Solution by James C. (https://github.com/JamesMCo)

import os, sys
sys.path.append(os.path.abspath("../.."))
import unittest, util.read
from util.tests import run

from collections import deque
from itertools import combinations

def solve(puzzle_input, preamble_size=25):
    working = deque(puzzle_input[:preamble_size])

    for n in puzzle_input[preamble_size:]:
        if not any(a + b == n for a, b in combinations(working, 2)):
            return n

        working.popleft()
        working.append(n)

def main():
    puzzle_input = util.read.as_int_list("\n")

    n = solve(puzzle_input)

    print("The first number that does not follow the property is " + str(n) + ".")

class AOC_Tests(unittest.TestCase):
    def test_ex1(self):
        return self.assertEqual(solve([ 35,  20,  15,  25,  47,
                                        40,  62,  55,  65,  95,
                                       102, 117, 150, 182, 127,
                                       219, 299, 277, 309, 576], 5), 127)

run(main)
