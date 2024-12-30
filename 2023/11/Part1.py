#!/usr/bin/env python3

#Advent of Code
#2023 Day 11, Part 1
#Solution by James C. (https://github.com/JamesMCo)

import os, sys
sys.path.append(os.path.abspath("../.."))
import unittest, util.read
from util.tests import run

from itertools import combinations

def solve(puzzle_input: list[str]) -> int:
    empty_rows: list[int] = [i for i, row in enumerate(puzzle_input) if all(col == "." for col in row)]
    empty_cols: list[int] = [i for i in range(len(puzzle_input[0])) if all(row[i] == "." for row in puzzle_input)]

    galaxies: list[tuple[int, int]] = []
    for y, row in enumerate(puzzle_input):
        for x, col in enumerate(row):
            if col == "#":
                galaxies.append((x, y))

    def manhattan_distance_respecting_expansion(x1: int, y1: int, x2: int, y2: int) -> int:
        expanded_cols = sum(1 for n in empty_cols if min(x1, x2) < n < max(x1, x2))
        expanded_rows = sum(1 for n in empty_rows if min(y1, y2) < n < max(y1, y2))
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
                                       "#...#....."]), 374)

if __name__ == "__main__":
    run(main)
