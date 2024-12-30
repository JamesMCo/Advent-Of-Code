#!/usr/bin/env python3

#Advent of Code
#2024 Day 4, Part 1
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
        while 0 <= u < width and 0 <= v < height and len(result) < 4:
            result += puzzle_input[v][u]
            u += du
            v += dv
        return result == "XMAS"

    found: int = 0
    for y, row in enumerate(puzzle_input):
        for x, c in enumerate(row):
            if c == "X":
                found += sum(scan_in_direction(x, y, dx, dy) for dx in range(-1, 2) for dy in range(-1, 2) if not (dx == 0 and dy == 0))

    return found

def main() -> tuple[str, int]:
    puzzle_input = util.read.as_lines()

    return "The number of times the word XMAS appears in the word search is {}.", solve(puzzle_input)

class AOC_Tests(unittest.TestCase):
    def test_ex1(self):
        return self.assertEqual(solve(["..X...",
                                       ".SAMX.",
                                       ".A..A.",
                                       "XMAS.S",
                                       ".X...."]), 4)

    def test_ex2(self):
        return self.assertEqual(solve(["MMMSXXMASM",
                                       "MSAMXMSMSA",
                                       "AMXSXMAAMM",
                                       "MSAMASMSMX",
                                       "XMASAMXAMM",
                                       "XXAMMXXAMA",
                                       "SMSMSASXSS",
                                       "SAXAMASAAA",
                                       "MAMMMXMMMM",
                                       "MXMXAXMASX"]), 18)

if __name__ == "__main__":
    run(main)
