#!/usr/bin/env python3

#Advent of Code
#2024 Day 3, Part 2
#Solution by James C. (https://github.com/JamesMCo)

import os, sys
sys.path.append(os.path.abspath("../.."))
import unittest, util.read
from util.tests import run

import re

def solve(puzzle_input: str) -> int:
    inst_pattern: re.Pattern = re.compile(r"mul\((\d{1,3}),(\d{1,3})\)|(do\(\))|(don't\(\))")
    enabled: bool = True
    total: int = 0

    for a, b, do, dont in re.findall(inst_pattern, puzzle_input):
        if enabled and a and b:
            total += int(a) * int(b)
        elif do:
            enabled = True
        elif dont:
            enabled = False

    return total

def main() -> tuple[str, int]:
    puzzle_input = util.read.as_string()

    return "The sum of the results of the multiplications is {}.", solve(puzzle_input)

class AOC_Tests(unittest.TestCase):
    def test_ex1(self):
        return self.assertEqual(solve("xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))"), 48)

run(main)
