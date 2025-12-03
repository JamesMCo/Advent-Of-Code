#!/usr/bin/env python3

#Advent of Code
#2025 Day 3, Part 2
#Solution by James C. (https://github.com/JamesMCo)

import os, sys
sys.path.append(os.path.abspath("../.."))
import unittest, util.read
from util.tests import run

from pathos.pools import ProcessPool as Pool

def solve(puzzle_input: list[str]) -> int:
    def find_max(bank: str, required: int = 12, cache: dict[tuple[str, int], int] = None) -> int:
        if cache is None:
            cache = {}

        if len(bank) < required:
            return 0
        elif required == 1:
            return max([int(b) for b in bank])
        else:
            if (bank, required) in cache:
                return cache[(bank, required)]

            max_found = 0
            for i in range(len(bank) - 1, -1, -1):
                if sub_search := find_max(bank[i+1:], required - 1, cache):
                    max_found = max(max_found, int(f"{bank[i]}{sub_search}"))
            cache[(bank, required)] = max_found
            return max_found

    with Pool() as pool:
        return sum(pool.map(find_max, puzzle_input))

def main() -> tuple[str, int]:
    puzzle_input = util.read.as_lines()

    return "The total output joltage is {}.", solve(puzzle_input)

class AOC_Tests(unittest.TestCase):
    def test_ex1(self):
        return self.assertEqual(solve(["987654321111111",
                                       "811111111111119",
                                       "234234234234278",
                                       "818181911112111"]), 3121910778619)

if __name__ == "__main__":
    run(main)
