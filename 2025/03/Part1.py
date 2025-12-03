#!/usr/bin/env python3

#Advent of Code
#2025 Day 3, Part 1
#Solution by James C. (https://github.com/JamesMCo)

import os, sys
sys.path.append(os.path.abspath("../.."))
import unittest, util.read
from util.tests import run

def solve(puzzle_input: list[str]) -> int:
    def find_max(bank: str) -> int:
        batteries: list[int] = [int(b) for b in bank]
        tens: int = batteries[0]
        units: int | None = None

        for i, battery in enumerate(batteries[1:], 1):
            if i != len(batteries) - 1 and battery > tens:
                tens = battery
                units = None
            elif units is None or battery > units:
                units = battery

        return tens * 10 + units

    return sum(map(find_max, puzzle_input))

def main() -> tuple[str, int]:
    puzzle_input = util.read.as_lines()

    return "The total output joltage is {}.", solve(puzzle_input)

class AOC_Tests(unittest.TestCase):
    def test_ex1(self):
        return self.assertEqual(solve(["987654321111111",
                                       "811111111111119",
                                       "234234234234278",
                                       "818181911112111"]), 357)

if __name__ == "__main__":
    run(main)
