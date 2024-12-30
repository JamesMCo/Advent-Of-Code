#!/usr/bin/env python3

#Advent of Code
#2023 Day 11, Part 2
#Solution by James C. (https://github.com/JamesMCo)

import os, sys
sys.path.append(os.path.abspath("../.."))
import unittest, util.read
from util.tests import run

from itertools import combinations

def solve(puzzle_input: list[str], age: int = 1_000_000) -> int:
    empty_rows: list[int] = [i for i, row in enumerate(puzzle_input) if all(col == "." for col in row)]
    empty_cols: list[int] = [i for i in range(len(puzzle_input[0])) if all(row[i] == "." for row in puzzle_input)]

    galaxies: list[tuple[int, int]] = []
    for y, row in enumerate(puzzle_input):
        for x, col in enumerate(row):
            if col == "#":
                galaxies.append((x, y))

    def manhattan_distance_respecting_expansion(x1: int, y1: int, x2: int, y2: int) -> int:
        # Age - 1, because the puzzle description states:
        #
        # "...make each empty row or column one million times larger.
        # That is, each empty row should be replaced with 1000000 empty rows,
        # and each empty column should be replaced with 1000000 empty columns."
        #
        # This means that we need to replace the original row/col, or rather,
        # add 999,999 empty rows/cols. Hence, age - 1.
        # This means that Part 1 could be adjusted to use an age parameter too,
        # with the default value being 2.

        expanded_cols = sum(age - 1 for n in empty_cols if min(x1, x2) < n < max(x1, x2))
        expanded_rows = sum(age - 1 for n in empty_rows if min(y1, y2) < n < max(y1, y2))
        return abs(x1 - x2) + expanded_rows + abs(y1 - y2) + expanded_cols

    return sum(manhattan_distance_respecting_expansion(*a, *b) for a, b in combinations(galaxies, 2))

def main() -> tuple[str, int]:
    puzzle_input = util.read.as_lines()

    return "The sum of the shortest paths between all galaxies is {}.", solve(puzzle_input)

class AOC_Tests(unittest.TestCase):
    def test_ex1(self):
        return self.assertEqual(solve(["...#......",
                                       ".......#..",
                                       "#.........",
                                       "..........",
                                       "......#...",
                                       ".#........",
                                       ".........#",
                                       "..........",
                                       ".......#..",
                                       "#...#....."], 10), 1030)

    def test_ex2(self):
        return self.assertEqual(solve(["...#......",
                                       ".......#..",
                                       "#.........",
                                       "..........",
                                       "......#...",
                                       ".#........",
                                       ".........#",
                                       "..........",
                                       ".......#..",
                                       "#...#....."], 100), 8410)

if __name__ == "__main__":
    run(main)
