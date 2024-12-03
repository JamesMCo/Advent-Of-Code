#!/usr/bin/env python3

#Advent of Code
#2024 Day 3, Part 1
#Solution by James C. (https://github.com/JamesMCo)

import os, sys
sys.path.append(os.path.abspath("../.."))
import unittest, util.read
from util.tests import run

import re

def solve(puzzle_input: str) -> int:
    mul_pattern: re.Pattern = re.compile(r"mul\((\d+),(\d+)\)")

    return sum(int(a) * int(b) for a, b in re.findall(mul_pattern, puzzle_input))

def main() -> tuple[str, int]:
    puzzle_input = util.read.as_string()

    return "The sum of the results of the multiplications is {}.", solve(puzzle_input)

class AOC_Tests(unittest.TestCase):
    def test_ex1(self):
        return self.assertEqual(solve("xmul(2,4)%&mul[3,7]!@^do_not_mul(5,5)+mul(32,64]then(mul(11,8)mul(8,5))"), 161)

run(main)
