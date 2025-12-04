#!/usr/bin/env python3

#Advent of Code
#2025 Day 4, Part 1
#Solution by James C. (https://github.com/JamesMCo)

import os, sys
sys.path.append(os.path.abspath("../.."))
import unittest, util.read
from util.tests import run

from typing import Iterable

def solve(puzzle_input: list[str]) -> int:
    max_width: int = len(puzzle_input[0]) - 1
    max_height: int = len(puzzle_input) - 1

    def neighbour_coords(x: int, y: int) -> Iterable[tuple[int, int]]:
        for dx in range(-1, 2):
            if not (0 <= x + dx <= max_width):
                continue
            for dy in range(-1, 2):
                if not (0 <= y + dy <= max_height) or (dx == 0 and dy == 0):
                    continue
                yield x + dx, y + dy

    def neighbours(x: int, y: int) -> Iterable[str]:
        yield from (puzzle_input[neighbour[1]][neighbour[0]] for neighbour in neighbour_coords(x, y))

    def neighbouring_paper(x: int, y: int) -> int:
        return sum(1 for neighbour in neighbours(x, y) if neighbour == "@")

    return sum(1 for y, row in enumerate(puzzle_input) for x, col in enumerate(row) if col == "@" and neighbouring_paper(x, y) < 4)

def main() -> tuple[str, int]:
    puzzle_input = util.read.as_lines()

    return "The number of rolls of paper that can be accessed by a forklift is {}.", solve(puzzle_input)

class AOC_Tests(unittest.TestCase):
    def test_ex1(self):
        return self.assertEqual(solve(["..@@.@@@@.",
                                       "@@@.@.@.@@",
                                       "@@@@@.@.@@",
                                       "@.@@@@..@.",
                                       "@@.@@@@.@@",
                                       ".@@@@@@@.@",
                                       ".@.@.@.@@@",
                                       "@.@@@.@@@@",
                                       ".@@@@@@@@.",
                                       "@.@.@@@.@."]), 13)

if __name__ == "__main__":
    run(main)
