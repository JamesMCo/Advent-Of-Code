#!/usr/bin/env python3

#Advent of Code
#2024 Day 11, Part 1
#Solution by James C. (https://github.com/JamesMCo)

import os, sys
sys.path.append(os.path.abspath("../.."))
import unittest, util.read
from util.tests import run

from functools import cache

def solve(puzzle_input: list[int], blinks: int = 25) -> int:
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

    return "The number of stones after blinking 25 times is {}.", solve(puzzle_input)

class AOC_Tests(unittest.TestCase):
    def test_ex1(self):
        return self.assertEqual(solve(list(map(int, "0 1 10 99 999".split(" "))), 1), 7)

    def test_ex2(self):
        return self.assertEqual(solve(list(map(int, "125 17".split(" "))), 6), 22)

    def test_ex3(self):
        return self.assertEqual(solve(list(map(int, "125 17".split(" ")))), 55312)

if __name__ == "__main__":
    run(main)
