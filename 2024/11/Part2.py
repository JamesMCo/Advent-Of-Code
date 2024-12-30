#!/usr/bin/env python3

#Advent of Code
#2024 Day 11, Part 2
#Solution by James C. (https://github.com/JamesMCo)

import os, sys
sys.path.append(os.path.abspath("../.."))
import unittest, util.read
from util.tests import run

from functools import cache

def solve(puzzle_input: list[int], blinks: int = 75) -> int:
    @cache
    def blink(stone: int, remaining_blinks: int = blinks) -> int:
        if remaining_blinks == 0:
            return 1
        elif stone == 0:
            return blink(1, remaining_blinks - 1)
        elif (digits := len(stone_str := str(stone))) % 2 == 0:
            return blink(int(stone_str[:digits // 2]), remaining_blinks - 1) +\
                   blink(int(stone_str[digits // 2:]), remaining_blinks - 1)
        else:
            return blink(stone * 2024, remaining_blinks - 1)

    return sum(map(blink, puzzle_input))

def main() -> tuple[str, int]:
    puzzle_input = util.read.as_int_list(" ")

    return "The number of stones after blinking 75 times is {}.", solve(puzzle_input)

class AOC_Tests(unittest.TestCase):
    @unittest.skip("No test cases")
    def test_ex1(self):
        pass

if __name__ == "__main__":
    run(main)
