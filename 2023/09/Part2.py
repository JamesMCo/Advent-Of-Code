#!/usr/bin/env python3

#Advent of Code
#2023 Day 9, Part 2
#Solution by James C. (https://github.com/JamesMCo)

import os, sys
sys.path.append(os.path.abspath("../.."))
import unittest, util.read
from util.tests import run

def solve(puzzle_input: list[str]) -> int:
    def extrapolate(ns: list[int]) -> int:
        if all(n == 0 for n in ns):
            return 0
        return ns[0] - extrapolate([n1 - n for n, n1 in zip(ns[:-1], ns[1:])])

    return sum(map(extrapolate, [[int(n) for n in line.split()] for line in puzzle_input]))

def main() -> tuple[str, int]:
    puzzle_input = util.read.as_lines()

    return "The sum of the extrapolated values is {}.", solve(puzzle_input)

class AOC_Tests(unittest.TestCase):
    def test_ex1(self):
        return self.assertEqual(solve(["0 3 6 9 12 15",
                                       "1 3 6 10 15 21",
                                       "10 13 16 21 30 45"]), 2)

run(main)
