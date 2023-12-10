#!/usr/bin/env python3

#Advent of Code
#2023 Day 10, Part 1
#Solution by James C. (https://github.com/JamesMCo)

import os, sys
sys.path.append(os.path.abspath("../.."))
import unittest, util.read
from util.tests import run

from util.two_d_world import World

def solve(puzzle_input: list[str]) -> int:
    pipes = World(".")
    pipes.load_from_lists(puzzle_input)

    start: tuple[int, int] | None = None
    for y, row in enumerate(puzzle_input):
        if "S" in row:
            start = (row.index("S"), y)
            break

    branches: list[tuple[tuple[int, int], str]] = []
    for (dx, dy, d, valid) in [
        ( 0, -1, "U", "|7F"), # Up
        ( 1,  0, "R", "-J7"), # Right
        ( 0,  1, "D", "|LJ"), # Down
        (-1,  0, "L", "-LF")  # Left
    ]:
        neighbour = (start[0] + dx, start[1] + dy)
        if pipes.in_bounds(*neighbour) and pipes[neighbour] in valid:
            branches.append((neighbour, d))

    distances: dict[tuple[int, int], int] = {start: 0} | {b[0]: 1 for b in branches}

    while True:
        for i, (coord, direction) in enumerate(branches):
            match direction, pipes[coord]:
                case "U", "|": new_direction = "U"
                case "U", "7": new_direction = "L"
                case "U", "F": new_direction = "R"

                case "R", "-": new_direction = "R"
                case "R", "J": new_direction = "U"
                case "R", "7": new_direction = "D"

                case "D", "|": new_direction = "D"
                case "D", "L": new_direction = "R"
                case "D", "J": new_direction = "L"

                case "L", "-": new_direction = "L"
                case "L", "L": new_direction = "U"
                case "L", "F": new_direction = "D"

            match new_direction:
                case "U": new_coord = (coord[0],     coord[1] - 1)
                case "R": new_coord = (coord[0] + 1, coord[1])
                case "D": new_coord = (coord[0],     coord[1] + 1)
                case "L": new_coord = (coord[0] - 1, coord[1])

            if new_coord in distances:
                # We've reached the far side of the loop
                # The maximum distance is either the pipe
                # that we were on, or the one that we've
                # just moved to.
                return max(distances[coord], distances[new_coord])

            distances[new_coord] = distances[coord] + 1
            branches[i] = (new_coord, new_direction)

def main() -> tuple[str, int]:
    puzzle_input = util.read.as_lines()

    return "The farthest point from the starting position is {} steps along the loop.", solve(puzzle_input)

class AOC_Tests(unittest.TestCase):
    def test_ex1(self):
        return self.assertEqual(solve(["-L|F7",
                                       "7S-7|",
                                       "L|7||",
                                       "-L-J|",
                                       "L|-JF"]), 4)

    def test_ex2(self):
        return self.assertEqual(solve(["..F7.",
                                       ".FJ|.",
                                       "SJ.L7",
                                       "|F--J",
                                       "LJ..."]), 8)

run(main)
