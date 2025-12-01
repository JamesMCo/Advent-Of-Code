#!/usr/bin/env python3

#Advent of Code
#2025 Day 1, Part 1
#Solution by James C. (https://github.com/JamesMCo)

import os, sys
sys.path.append(os.path.abspath("../.."))
import unittest, util.read
from util.tests import run

def solve(puzzle_input: list[str]) -> int:
    pointing = 50
    count = 0

    for instruction in puzzle_input:
        rotation = int(instruction[1:]) * (1 if instruction[0] == "R" else -1)
        pointing = (pointing + rotation) % 100
        if pointing == 0:
            count += 1

    return count

def main() -> tuple[str, int]:
    puzzle_input = util.read.as_lines()

    return "The password to open the door is {}.", solve(puzzle_input)

class AOC_Tests(unittest.TestCase):
    def test_ex1(self):
        return self.assertEqual(solve(["L68",
                                       "L30",
                                       "R48",
                                       "L5",
                                       "R60",
                                       "L55",
                                       "L1",
                                       "L99",
                                       "R14",
                                       "L82"]), 3)

if __name__ == "__main__":
    run(main)
