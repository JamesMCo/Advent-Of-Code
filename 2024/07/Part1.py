#!/usr/bin/env python3

#Advent of Code
#2024 Day 7, Part 1
#Solution by James C. (https://github.com/JamesMCo)

import os, sys
sys.path.append(os.path.abspath("../.."))
import unittest, util.read
from util.tests import run

def solve(puzzle_input: list[str]) -> int:
    def is_possible(target: int, acc: int, numbers: list[int], length: int, current: int = 0) -> bool:
        if current == length:
            return target == acc
        elif acc > target:
            # Operations do not allow getting smaller (subtract, divide, etc.)
            # so if any number is larger than the target, it's now impossible
            return False
        else:
            return is_possible(target, acc + numbers[current], numbers, length, current + 1)\
                or is_possible(target, acc * numbers[current], numbers, length, current + 1)

    return sum([
        int(line.split()[0][:-1])
        for line in puzzle_input
        if is_possible(
            int(line.split()[0][:-1]),          # Target value
            int(line.split()[1]),               # First of the remaining numbers
            [int(n) for n in line.split()[2:]], # Rest of the remaining numbers
            len(line.split()) - 2,              # How many remaining numbers (not counting the first) to iterate over (i.e. how many operators need to add)
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
