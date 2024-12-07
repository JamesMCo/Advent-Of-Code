#!/usr/bin/env python3

#Advent of Code
#2024 Day 7, Part 1
#Solution by James C. (https://github.com/JamesMCo)

import os, sys
sys.path.append(os.path.abspath("../.."))
import unittest, util.read
from util.tests import run

def solve(puzzle_input: list[str]) -> int:
    def is_possible(target: int, numbers: list[int]) -> bool:
        if len(numbers) == 1:
            return target == numbers[0]
        elif numbers[0] > target:
            # Operations do not allow getting smaller (subtract, divide, etc.)
            # so if any number is larger than the target, it's now impossible
            return False
        else:
            return is_possible(target, [numbers[0] + numbers[1]] + numbers[2:])\
                or is_possible(target, [numbers[0] * numbers[1]] + numbers[2:])

    return sum([
        int(line.split()[0][:-1])
        for line in puzzle_input
        if is_possible(
            int(line.split()[0][:-1]),         # Target value (left of colon, without including colon)
            [int(n) for n in line.split()[1:]] # Remaining numbers (right of colon)
        )
    ])

def main() -> tuple[str, int]:
    puzzle_input = util.read.as_lines()

    return "The total calibration result is {}.", solve(puzzle_input)

class AOC_Tests(unittest.TestCase):
    def test_ex1(self):
        return self.assertEqual(solve(["190: 10 19",
                                       "3267: 81 40 27",
                                       "83: 17 5",
                                       "156: 15 6",
                                       "7290: 6 8 6 15",
                                       "161011: 16 10 13",
                                       "192: 17 8 14",
                                       "21037: 9 7 18 13",
                                       "292: 11 6 16 20"]), 3749)

run(main)
