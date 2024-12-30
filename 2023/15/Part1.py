#!/usr/bin/env python3

#Advent of Code
#2023 Day 15, Part 1
#Solution by James C. (https://github.com/JamesMCo)

import os, sys
sys.path.append(os.path.abspath("../.."))
import unittest, util.read
from util.tests import run

def solve(puzzle_input: list[str]) -> int:
    def HASH(s) -> int:
        current_value = 0
        for c in s:
            current_value = ((current_value + ord(c)) * 17) % 256
        return current_value

    return sum(map(HASH, puzzle_input))

def main() -> tuple[str, int]:
    puzzle_input = util.read.as_string_list(",")

    return "The sum of the hashes is {}.", solve(puzzle_input)

class AOC_Tests(unittest.TestCase):
    def test_ex1(self):
        return self.assertEqual(solve(["rn=1", "cm-", "qp=3", "cm=2", "qp-", "pc=4", "ot=9", "ab=5", "pc-", "pc=6", "ot=7"]), 1320)

if __name__ == "__main__":
    run(main)
