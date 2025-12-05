#!/usr/bin/env python3

#Advent of Code
#2025 Day 5, Part 1
#Solution by James C. (https://github.com/JamesMCo)

import os, sys
sys.path.append(os.path.abspath("../.."))
import unittest, util.read
from util.tests import run

from itertools import takewhile

def solve(puzzle_input: list[str]) -> int:
    def parse_range(range_description: str) -> range:
        lower, upper = range_description.split("-")
        return range(int(lower), int(upper) + 1)
    ranges: list[range] = list(map(parse_range, takewhile(lambda l: l != "", puzzle_input)))

    return len([
        ingredient
        for ingredient in map(int, puzzle_input[len(ranges) + 1:])
        if any(ingredient in r for r in ranges)
    ])

def main() -> tuple[str, int]:
    puzzle_input = util.read.as_lines()

    return "The number of fresh ingredients is {}.", solve(puzzle_input)

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
                                       "32"]), 3)

if __name__ == "__main__":
    run(main)
