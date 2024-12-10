#!/usr/bin/env python3

#Advent of Code
#2024 Day 10, Part 2
#Solution by James C. (https://github.com/JamesMCo)

import os, sys
sys.path.append(os.path.abspath("../.."))
import unittest, util.read
from util.tests import run

from functools import cache

def solve(puzzle_input: list[str]) -> int:
    area: list[list[int]] = [[int(col) if col != "." else -10 for col in row] for row in puzzle_input]
    x_bounds: range = range(0, len(area[0]))
    y_bounds: range = range(0, len(area))

    @cache
    def find_nines(start: tuple[int, int]) -> int:
        if (current_elevation := area[start[1]][start[0]]) == 9:
            return 1

        found_nines: int = 0
        for dx, dy in [(-1, 0), (0, 1), (1, 0), (0, -1)]:
            if start[0] + dx in x_bounds and start[1] + dy in y_bounds:
                if area[start[1] + dy][start[0] + dx] == current_elevation + 1:
                    found_nines += find_nines((start[0] + dx, start[1] + dy))
        return found_nines

    return sum(find_nines((x, y)) for y in range(len(area)) for x in range(len(area[0])) if area[y][x] == 0)

def main() -> tuple[str, int]:
    puzzle_input = util.read.as_lines()

    return "The sum of the ratings of all trailheads is {}.", solve(puzzle_input)

class AOC_Tests(unittest.TestCase):
    def test_ex1(self):
        return self.assertEqual(solve([".....0.",
                                       "..4321.",
                                       "..5..2.",
                                       "..6543.",
                                       "..7..4.",
                                       "..8765.",
                                       "..9...."]), 3)

    def test_ex2(self):
        return self.assertEqual(solve(["012345",
                                       "123456",
                                       "234567",
                                       "345678",
                                       "4.6789",
                                       "56789."]), 227)

    def test_ex3(self):
        return self.assertEqual(solve(["89010123",
                                       "78121874",
                                       "87430965",
                                       "96549874",
                                       "45678903",
                                       "32019012",
                                       "01329801",
                                       "10456732"]), 81)

run(main)
