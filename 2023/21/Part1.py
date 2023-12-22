#!/usr/bin/env python3

#Advent of Code
#2023 Day 21, Part 1
#Solution by James C. (https://github.com/JamesMCo)

import os, sys
sys.path.append(os.path.abspath("../.."))
import unittest, util.read
from util.tests import run

def solve(puzzle_input: list[str], steps = 64) -> int:
    empty: set[tuple[int, int]] = set()
    locations: set[tuple[int, int]] = set()

    for y, row in enumerate(puzzle_input):
        for x, col in enumerate(row):
            match col:
                case "#":
                    pass
                case ".":
                    empty.add((x, y))
                case "S":
                    empty.add((x, y))
                    locations.add((x, y))

    for _ in range(steps):
        new_locations: set[tuple[int, int]] = set()

        for (x, y) in locations:
            for (dx, dy) in ((0, -1), (1, 0), (0, 1), (-1, 0)):
                if (x + dx, y + dy) in empty:
                    new_locations.add((x + dx, y + dy))

        locations = new_locations

    return len(locations)

def main() -> tuple[str, int]:
    puzzle_input = util.read.as_lines()

    return "The number of garden plots that the Elf could reach in exactly 64 steps is {}.", solve(puzzle_input)

class AOC_Tests(unittest.TestCase):
    def test_ex1(self):
        return self.assertEqual(solve(["...........",
                                       ".....###.#.",
                                       ".###.##..#.",
                                       "..#.#...#..",
                                       "....#.#....",
                                       ".##..S####.",
                                       ".##..#...#.",
                                       ".......##..",
                                       ".##.#.####.",
                                       ".##..##.##.",
                                       "..........."], 6), 16)

run(main)
