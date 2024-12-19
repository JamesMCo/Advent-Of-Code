#!/usr/bin/env python3

#Advent of Code
#2024 Day 19, Part 1
#Solution by James C. (https://github.com/JamesMCo)

import os, sys
sys.path.append(os.path.abspath("../.."))
import unittest, util.read
from util.tests import run

from functools import cache

def solve(puzzle_input: list[str]) -> int:
    patterns: dict[str, list[str]] = {start_letter: [] for start_letter in "wubrg"}
    for pattern in puzzle_input[0].split(", "):
        patterns[pattern[0]].append(pattern)

    @cache
    def possible(towel: str) -> bool:
        if len(towel) == 0:
            return True
        return any(possible(towel[len(pattern):]) for pattern in patterns[towel[0]] if towel.startswith(pattern))

    return sum(1 for design in puzzle_input[2:] if possible(design))

def main() -> tuple[str, int]:
    puzzle_input = util.read.as_lines()

    return "The number of possible designs is {}.", solve(puzzle_input)

class AOC_Tests(unittest.TestCase):
    def test_ex1(self):
        return self.assertEqual(solve(["r, wr, b, g, bwu, rb, gb, br",
                                       "",
                                       "brwrr",
                                       "bggr",
                                       "gbbr",
                                       "rrbgbr",
                                       "ubwu",
                                       "bwurrg",
                                       "brgr",
                                       "bbrgwb"]), 6)

run(main)
