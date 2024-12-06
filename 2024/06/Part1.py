#!/usr/bin/env python3

#Advent of Code
#2024 Day 6, Part 1
#Solution by James C. (https://github.com/JamesMCo)

import os, sys
sys.path.append(os.path.abspath("../.."))
import unittest, util.read
from util.tests import run

from util.two_d_world import World

def solve(puzzle_input: list[str]) -> int:
    area: World = World(".")
    area.load_from_lists(puzzle_input)

    guard_loc: complex | None = None
    guard_dir: complex = 0 - 1j
    for y in range(area.min_y, area.max_y + 1):
        for x in range(area.min_x, area.max_x + 1):
            if area[(x, y)] == "^":
                guard_loc = complex(x, y)
                area[(x, y)] = "."
                break
        if guard_loc is not None:
            break

    visited: set[complex] = set()
    while True:
        visited.add(guard_loc)
        next_step: complex = guard_loc + guard_dir
        if area.in_bounds(int(next_step.real), int(next_step.imag)):
            match area[(int(next_step.real), int(next_step.imag))]:
                case ".":
                    guard_loc = next_step
                case "#":
                    guard_dir *= complex(0, 1)
        else:
            return len(visited)

def main() -> tuple[str, int]:
    puzzle_input = util.read.as_lines()

    return "The number of distinct positions visited by the guard is {}.", solve(puzzle_input)

class AOC_Tests(unittest.TestCase):
    def test_ex1(self):
        return self.assertEqual(solve(["....#.....",
                                       ".........#",
                                       "..........",
                                       "..#.......",
                                       ".......#..",
                                       "..........",
                                       ".#..^.....",
                                       "........#.",
                                       "#.........",
                                       "......#..."]), 41)

run(main)
