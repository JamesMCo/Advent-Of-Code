#!/usr/bin/env python3

#Advent of Code
#2025 Day 1, Part 2
#Solution by James C. (https://github.com/JamesMCo)

import os, sys
sys.path.append(os.path.abspath("../.."))
import unittest, util.read
from util.tests import run

def solve(puzzle_input: list[str]) -> int:
    pointing = 50
    count = 0

    for instruction in puzzle_input:
        rotation = int(instruction[1:])
        if rotation >= 100:
            count += rotation // 100
            rotation %= 100
        rotation *= 1 if instruction[0] == "R" else -1

        if pointing == 0:
            # Only want to count clicks that enter the 0 state, not leave it
            pointing = (pointing + rotation) % 100
        else:
            pointing += rotation
            if rotation < 0 and pointing <= 0:
                count += 1
            elif rotation > 0 and pointing >= 100:
                count += 1
            pointing %= 100

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
                                       "L82"]), 6)

if __name__ == "__main__":
    run(main)
