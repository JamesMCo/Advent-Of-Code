#!/usr/bin/env python3

#Advent of Code
#2025 Day 6, Part 1
#Solution by James C. (https://github.com/JamesMCo)

import os, sys
sys.path.append(os.path.abspath("../.."))
import unittest, util.read
from util.tests import run

from math import prod

def solve(puzzle_input: list[str]) -> int:
    numbers: list[list[int]] = [list(map(int, line.strip().split())) for line in puzzle_input[:-1]]
    operators: list[str] = puzzle_input[-1].strip().split()

    grand_total: int = 0
    for nums, op in zip(zip(*numbers), operators):
        match op:
            case "+":
                grand_total += sum(nums)
            case "*":
                grand_total += prod(nums)

    return grand_total

def main() -> tuple[str, int]:
    puzzle_input = util.read.as_lines_only_rstrip()

    return "The grand total is {}.", solve(puzzle_input)

class AOC_Tests(unittest.TestCase):
    def test_ex1(self):
        return self.assertEqual(solve(["123 328  51 64 ",
                                       " 45 64  387 23 ",
                                       "  6 98  215 314",
                                       "*   +   *   +  "]), 4277556)

if __name__ == "__main__":
    run(main)
