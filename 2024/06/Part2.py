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

    guard_start_loc: complex | None = None
    guard_start_dir: complex = 0 - 1j
    for y in range(area.min_y, area.max_y + 1):
        for x in range(area.min_x, area.max_x + 1):
            if area[(x, y)] == "^":
                guard_start_loc = complex(x, y)
                area[(x, y)] = "."
                break
        if guard_start_loc is not None:
            break

    def candidate_obstructions() -> set[complex]:
        guard_loc: complex = guard_start_loc
        guard_dir: complex = guard_start_dir
        walked: set[complex] = set()
        while True:
            if guard_loc != guard_start_loc:
                walked.add(guard_loc)
            next_step: complex = guard_loc + guard_dir
            if area.in_bounds(int(next_step.real), int(next_step.imag)):
                match area[(int(next_step.real), int(next_step.imag))]:
                    case ".":
                        guard_loc = next_step
                    case "#":
                        guard_dir *= complex(0, 1)
            else:
                return walked

    def causes_loop(obst_loc: complex) -> bool:
        guard_loc: complex = guard_start_loc
        guard_dir: complex = guard_start_dir
        walked: set[tuple[complex, complex]] = set()
        while True:
            if (guard_loc, guard_dir) in walked:
                return True
            walked.add((guard_loc, guard_dir))
            next_step: complex = guard_loc + guard_dir
            if area.in_bounds(int(next_step.real), int(next_step.imag)):
                if next_step == obst_loc:
                    guard_dir *= complex(0, 1)
                else:
                    match area[(int(next_step.real), int(next_step.imag))]:
                        case ".":
                            guard_loc = next_step
                        case "#":
                            guard_dir *= complex(0, 1)
            else:
                return False

    return len([candidate for candidate in candidate_obstructions() if causes_loop(candidate)])

def main() -> tuple[str, int]:
    puzzle_input = util.read.as_lines()

    return "The number of positions in which an obstruction that would cause a loop is {}.", solve(puzzle_input)

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
                                       "......#..."]), 6)

run(main)
