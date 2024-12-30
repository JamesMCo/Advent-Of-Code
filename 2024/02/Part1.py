#!/usr/bin/env python3

#Advent of Code
#2024 Day 2, Part 1
#Solution by James C. (https://github.com/JamesMCo)

import os, sys
sys.path.append(os.path.abspath("../.."))
import unittest, util.read
from util.tests import run

def solve(puzzle_input: list[str]) -> int:
    def is_safe(report: list[int]) -> bool:
        # None if not yet determined
        ascending: bool | None = None

        for a, b in zip(report, report[1:]):
            if ascending is None:
                ascending = a < b

            if a == b:
                return False
            elif ascending and a > b:
                return False
            elif not ascending and a < b:
                return False
            elif not (-3 <= b - a <= 3):
                return False

        # If no delta between adjacent pairs of numbers
        # fails any test, then the report is safe
        return True

    return len(list(filter(is_safe, [[int(x) for x in line.split()] for line in puzzle_input])))

def main() -> tuple[str, int]:
    puzzle_input = util.read.as_lines()

    return "The number of safe reports is {}.", solve(puzzle_input)

class AOC_Tests(unittest.TestCase):
    def test_ex1(self):
        return self.assertEqual(solve(["7 6 4 2 1",
                                       "1 2 7 8 9",
                                       "9 7 6 2 1",
                                       "1 3 2 4 5",
                                       "8 6 4 4 1",
                                       "1 3 6 7 9"]), 2)

if __name__ == "__main__":
    run(main)
