#!/usr/bin/env python3

#Advent of Code
#2025 Day 6, Part 2
#Solution by James C. (https://github.com/JamesMCo)

import os, sys
sys.path.append(os.path.abspath("../.."))
import unittest, util.read
from util.tests import run

from itertools import zip_longest
from math import prod

def solve(puzzle_input: list[str]) -> int:
    grand_total: int = 0

    nums: list[int] = []
    op: str = ""

    def calculate():
        match op:
            case "+":
                return sum(nums)
            case "*":
                return prod(nums)
            case _:
                return 0

    for cols in zip_longest(*puzzle_input, fillvalue=" "):
        if all(c == " " for c in cols):
            grand_total += calculate()
            nums = []
            op = ""
        else:
            current_num: str = ""
            for i, c in enumerate(cols[:-1]):
                if c != " ":
                    current_num += c
            if current_num != "":
                nums.append(int(current_num))

            if cols[-1] != " ":
                op = cols[-1]
    grand_total += calculate()

    return grand_total

def main() -> tuple[str, int]:
    puzzle_input = util.read.as_lines_only_rstrip()

    return "The grand total is {}.", solve(puzzle_input)

class AOC_Tests(unittest.TestCase):
    def test_ex1(self):
        return self.assertEqual(solve(["123 328  51 64 ",
                                       " 45 64  387 23 ",
                                       "  6 98  215 314",
                                       "*   +   *   +  "]), 3263827)

if __name__ == "__main__":
    run(main)
