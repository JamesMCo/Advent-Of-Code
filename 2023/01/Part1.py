#!/usr/bin/env python3

#Advent of Code
#2023 Day 1, Part 1
#Solution by James C. (https://github.com/JamesMCo)

import os, sys
sys.path.append(os.path.abspath("../.."))
import unittest, util.read
from util.tests import run

def solve(puzzle_input: list[str]) -> int:
    def parse_calibration_value(line: str) -> int:
        first, last = "", ""
        for c in line:
            if c.isdigit():
                first, last = first or c, c
        return int(f"{first}{last}")

    return sum(map(parse_calibration_value, puzzle_input))

def main() -> tuple[str, int]:
    puzzle_input = util.read.as_lines()

    return "The sum of all the calibration values is {}.", solve(puzzle_input)

class AOC_Tests(unittest.TestCase):
    def test_ex1(self):
        return self.assertEqual(solve(["1abc2",
                                       "pqr3stu8vwx",
                                       "a1b2c3d4e5f",
                                       "treb7uchet"]), 142)

if __name__ == "__main__":
    run(main)
