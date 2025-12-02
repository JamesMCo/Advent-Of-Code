#!/usr/bin/env python3

#Advent of Code
#2025 Day 2, Part 1
#Solution by James C. (https://github.com/JamesMCo)

import os, sys
sys.path.append(os.path.abspath("../.."))
import unittest, util.read
from util.tests import run

from pathos.pools import ProcessPool as Pool
import re

def solve(puzzle_input: list[str]) -> int:
    pattern: re.Pattern = re.compile(r"^(\d+)\1$")
    def test_range(id_range: str) -> int:
        lower, upper = id_range.split("-")
        return sum(candidate for candidate in range(int(lower), int(upper) + 1) if pattern.match(str(candidate)))

    with Pool() as pool:
        return sum(pool.map(test_range, puzzle_input))

def main() -> tuple[str, int]:
    puzzle_input = util.read.as_string_list(",")

    return "The sum of all of the invalid IDs is {}.", solve(puzzle_input)

class AOC_Tests(unittest.TestCase):
    def test_ex1(self):
        return self.assertEqual(solve(["11-22",
                                       "95-115",
                                       "998-1012",
                                       "1188511880-1188511890",
                                       "222220-222224",
                                       "1698522-1698528",
                                       "446443-446449",
                                       "38593856-38593862",
                                       "565653-565659",
                                       "824824821-824824827",
                                       "2121212118-2121212124"]), 1227775554)

if __name__ == "__main__":
    run(main)
