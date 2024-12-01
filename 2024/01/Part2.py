#!/usr/bin/env python3

#Advent of Code
#2024 Day 1, Part 2
#Solution by James C. (https://github.com/JamesMCo)

import os, sys
sys.path.append(os.path.abspath("../.."))
import unittest, util.read
from util.tests import run

from collections import defaultdict
import re

def solve(puzzle_input: list[str]) -> int:
    left: list[int] = []
    right: defaultdict[int, int] = defaultdict(int)

    for line in puzzle_input:
        left_n, right_n = re.match(r"(\d+)\s+(\d+)", line).groups()
        left.append(int(left_n))
        right[int(right_n)] += 1

    return sum(l * right[l] for l in left)

def main() -> tuple[str, int]:
    puzzle_input = util.read.as_lines()

    return "The similarity score of the lists is {}.", solve(puzzle_input)

class AOC_Tests(unittest.TestCase):
    def test_ex1(self):
        return self.assertEqual(solve(["3   4",
                                       "4   3",
                                       "2   5",
                                       "1   3",
                                       "3   9",
                                       "3   3"]), 31)

run(main)
