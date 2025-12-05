#!/usr/bin/env python3

#Advent of Code
#2025 Day 5, Part 2
#Solution by James C. (https://github.com/JamesMCo)

import os, sys
sys.path.append(os.path.abspath("../.."))
import unittest, util.read
from util.tests import run

from itertools import combinations, takewhile

def solve(puzzle_input: list[str]) -> int:
    def parse_range(range_description: str) -> tuple[int, int]:
        lower, upper = range_description.split("-")
        return int(lower), int(upper)
    ranges: list[tuple[int, int]] = list(map(parse_range, takewhile(lambda l: l != "", puzzle_input)))

    changed: bool = True
    while changed:
        changed = False
        for i, j in combinations(range(len(ranges)), 2):
            lower_i, upper_i = ranges[i]
            lower_j, upper_j = ranges[j]

            if lower_i <= lower_j <= upper_i or lower_i <= upper_j <= upper_i\
            or lower_j <= lower_i <= upper_j or lower_j <= upper_i <= upper_j:
                ranges.pop(j)
                ranges[i] = (min(lower_i, lower_j), max(upper_i, upper_j))
                changed = True
                break

    return sum(upper + 1 - lower for lower, upper in ranges)

def main() -> tuple[str, int]:
    puzzle_input = util.read.as_lines()

    return "The number of possible fresh ingredients is {}.", solve(puzzle_input)

class AOC_Tests(unittest.TestCase):
    def test_ex1(self):
        return self.assertEqual(solve(["3-5",
                                       "10-14",
                                       "16-20",
                                       "12-18",
                                       "",
                                       "1",
                                       "5",
                                       "8",
                                       "11",
                                       "17",
                                       "32"]), 14)

if __name__ == "__main__":
    run(main)
