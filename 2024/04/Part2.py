#!/usr/bin/env python3

#Advent of Code
#2024 Day 4, Part 2
#Solution by James C. (https://github.com/JamesMCo)

import os, sys
sys.path.append(os.path.abspath("../.."))
import unittest, util.read
from util.tests import run

def solve(puzzle_input: list[str]) -> int:
    width = len(puzzle_input[0])
    height = len(puzzle_input)

    def scan_in_direction(u: int, v: int, du: int, dv: int) -> bool:
        result: str = ""
        u -= du
        v -= dv
        while 0 <= u < width and 0 <= v < height and len(result) < 3:
            result += puzzle_input[v][u]
            u += du
            v += dv
        return result == "MAS" or result == "SAM"

    found: int = 0
    for y, row in enumerate(puzzle_input):
        for x, c in enumerate(row):
            if c == "A" and scan_in_direction(x, y, 1, 1) and scan_in_direction(x, y, 1, -1):
                found += 1

    return found

def main() -> tuple[str, int]:
    puzzle_input = util.read.as_lines()

    return "The number of times an X-MAS appears in the word search is {}.", solve(puzzle_input)

class AOC_Tests(unittest.TestCase):
    def test_ex1(self):
        return self.assertEqual(solve(["MMMSXXMASM",
                                       "MSAMXMSMSA",
                                       "AMXSXMAAMM",
                                       "MSAMASMSMX",
                                       "XMASAMXAMM",
                                       "XXAMMXXAMA",
                                       "SMSMSASXSS",
                                       "SAXAMASAAA",
                                       "MAMMMXMMMM",
                                       "MXMXAXMASX"]), 9)

run(main)
