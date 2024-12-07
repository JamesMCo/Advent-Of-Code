#!/usr/bin/env python3

#Advent of Code
#2024 Day 7, Part 1
#Solution by James C. (https://github.com/JamesMCo)

import os, sys
sys.path.append(os.path.abspath("../.."))
import unittest, util.read
from util.tests import run

import re
from typing import Iterator

def solve(puzzle_input: list[str]) -> int:
    def parse_line(line: str) -> tuple[int, int, list[int], int]:
        # By parsing the input line    |    |    |          > Number of remaining values after the first (i.e. how many operators need to be added)
        # in a separate function,      |    |    +----------> Rest of the remaining values
        # we can avoid multiple calls  |    +---------------> First of the remaining values
        # to, say, str.split()         +--------------------> Target value
        numbers: Iterator[int] = map(int, re.findall(r"\d+", line))

        target: int = next(numbers)
        acc: int = next(numbers)
        remaining = list(numbers)

        return target, acc, remaining, len(remaining)

    def is_possible(target: int, acc: int, numbers: list[int], length: int, current: int = 0) -> bool:
        if current == length:
            return target == acc
        elif acc > target:
            # Operations do not allow getting smaller (subtract, divide, etc.)
            # so if any number is larger than the target, it's now impossible
            return False
        else:
            return is_possible(target, acc + numbers[current], numbers, length, current + 1)\
                or is_possible(target, acc * numbers[current], numbers, length, current + 1)\
                or is_possible(target, int(f"{acc}{numbers[current]}"), numbers, length, current + 1)

    return sum([
        line[0]
        for line in map(parse_line, puzzle_input)
        if is_possible(*line)
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
                                       "292: 11 6 16 20"]), 11387)

run(main)
