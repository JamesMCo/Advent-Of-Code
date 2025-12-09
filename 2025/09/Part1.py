#!/usr/bin/env python3

#Advent of Code
#2025 Day 9, Part 1
#Solution by James C. (https://github.com/JamesMCo)

import os, sys
sys.path.append(os.path.abspath("../.."))
import unittest, util.read
from util.tests import run

from itertools import combinations

def solve(puzzle_input: list[str]) -> int:
    return max(
        (max(a[0] + 1, b[0] + 1) - min(a[0], b[0])) * (max(a[1], b[1]) - min(a[1], b[1]) + 1)
        for a, b in combinations(
            (tuple(map(int, l.split(","))) for l in puzzle_input),
            2
        )
    )

def main() -> tuple[str, int]:
    puzzle_input = util.read.as_lines()

    return "The largest area of any rectangle that can be made is {}.", solve(puzzle_input)

class AOC_Tests(unittest.TestCase):
    def test_ex1(self):
        return self.assertEqual(solve(["7,1",
                                       "11,1",
                                       "11,7",
                                       "9,7",
                                       "9,5",
                                       "2,5",
                                       "2,3",
                                       "7,3"]), 50)

if __name__ == "__main__":
    run(main)
