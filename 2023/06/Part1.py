#!/usr/bin/env python3

#Advent of Code
#2023 Day 6, Part 1
#Solution by James C. (https://github.com/JamesMCo)

import os, sys
sys.path.append(os.path.abspath("../.."))
import unittest, util.read
from util.tests import run

from math import prod
import re

def solve(puzzle_input: list[str]) -> int:
    def count_record_breaking_strategies(record_time: int, record_distance: int) -> int:
        total = 0
        for t in range(record_time):
            if t * (record_time - t) > record_distance:
                total += 1
        return total

    return prod(
        count_record_breaking_strategies(int(time), int(distance))
        for time, distance in zip(*[re.findall(r"\d+", line) for line in puzzle_input])
    )

def main() -> tuple[str, int]:
    puzzle_input = util.read.as_lines()

    return "The product of the number of ways you can beat each race's record is {}.", solve(puzzle_input)

class AOC_Tests(unittest.TestCase):
    def test_ex1(self):
        return self.assertEqual(solve(["Time:      7  15   30",
                                       "Distance:  9  40  200"]), 288)

run(main)
