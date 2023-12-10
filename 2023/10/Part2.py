#!/usr/bin/env python3

#Advent of Code
#2023 Day 10, Part 2
#Solution by James C. (https://github.com/JamesMCo)

import os, sys
sys.path.append(os.path.abspath("../.."))
import unittest, util.read
from util.tests import run

from collections import deque
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
    s_shape = ""
    for (dx, dy, d, valid) in [
        ( 0, -1, "U", "|7F"), # Up
        ( 1,  0, "R", "-J7"), # Right
        ( 0,  1, "D", "|LJ"), # Down
        (-1,  0, "L", "-LF")  # Left
    ]:
        neighbour = (start[0] + dx, start[1] + dy)
        if pipes.in_bounds(*neighbour) and pipes[neighbour] in valid:
            branches.append((neighbour, d))
            s_shape += d

    clean_pipes: dict[tuple[int, int], str] = {
        start: {"UR": "L", "UD": "|", "UL": "J", "RD": "F", "RL": "-", "DL": "7"}[s_shape]
    } | {b[0]: pipes[b[0]] for b in branches}
    all_pipes_found = False

    while not all_pipes_found:
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

            if new_coord in clean_pipes:
                # We've reached the far side of the loop
                all_pipes_found = True
                break

            clean_pipes[new_coord] = pipes[new_coord]
            branches[i] = (new_coord, new_direction)

    # Recreate the pipes World object using a default dict, which
    # will make lookups for non-pipes easier when flood filling
    # Also, inflate the grid by 3x to allow squeezing through gaps in pipes
    # e.g.
    #        .#.
    # L  =>  .##
    #        ...
    #
    pipes = World(".", True)
    inflated_pipes = {}
    for (x, y), pipe in clean_pipes.items():
        # Central cell
        inflated_pipes[((x * 3) + 1, (y * 3) + 1)] = "#"

        # Stretches up
        if pipe in "|LJ":
            inflated_pipes[((x * 3) + 1, y * 3)] = "#"

        # Stretches right
        if pipe in "-LF":
            inflated_pipes[((x * 3) + 2, (y * 3) + 1)] = "#"

        # Stretches down
        if pipe in "|7F":
            inflated_pipes[((x * 3) + 1, (y * 3) + 2)] = "#"

        # Stretches left
        if pipe in "-J7":
            inflated_pipes[(x * 3, (y * 3) + 1)] = "#"
    pipes.load_from_dict(inflated_pipes)

    outside: set[tuple[int, int]] = set()
    queued: deque[tuple[int, int]] = deque()
    queued.append((-1, -1))

    while queued:
        here = queued.popleft()
        outside.add(here)

        for (dx, dy) in [(0, -1), (1, 0), (0, 1), (-1, 0)]:
            neighbour = (here[0] + dx, here[1] + dy)

            # Ensure flood fill only allows one border cell around the entire map
            if not -1 <= neighbour[0] <= pipes.max_x + 1 or \
               not -1 <= neighbour[1] <= pipes.max_y + 1:
                continue

            # Ensure flood fill isn't repeating already visited cells
            if neighbour in outside or neighbour in queued:
                continue

            # Ensure flood fill is only propagating to non-pipe cells
            if pipes[neighbour] == ".":
                queued.append(neighbour)

    return sum(1 for x in range(1, pipes.max_x + 1, 3) for y in range(1, pipes.max_y + 1, 3) if (x, y) not in outside and (x, y) not in inflated_pipes)

def main() -> tuple[str, int]:
    puzzle_input = util.read.as_lines()

    return "The number of tiles enclosed by the loop is {}.", solve(puzzle_input)

class AOC_Tests(unittest.TestCase):
    def test_ex1(self):
        return self.assertEqual(solve(["...........",
                                       ".S-------7.",
                                       ".|F-----7|.",
                                       ".||.....||.",
                                       ".||.....||.",
                                       ".|L-7.F-J|.",
                                       ".|..|.|..|.",
                                       ".L--J.L--J.",
                                       "..........."]), 4)

    def test_ex2(self):
        return self.assertEqual(solve(["..........",
                                       ".S------7.",
                                       ".|F----7|.",
                                       ".||....||.",
                                       ".||....||.",
                                       ".|L-7F-J|.",
                                       ".|..||..|.",
                                       ".L--JL--J.",
                                       ".........."]), 4)

    def test_ex3(self):
        return self.assertEqual(solve([".F----7F7F7F7F-7....",
                                       ".|F--7||||||||FJ....",
                                       ".||.FJ||||||||L7....",
                                       "FJL7L7LJLJ||LJ.L-7..",
                                       "L--J.L7...LJS7F-7L7.",
                                       "....F-J..F7FJ|L7L7L7",
                                       "....L7.F7||L7|.L7L7|",
                                       ".....|FJLJ|FJ|F7|.LJ",
                                       "....FJL-7.||.||||...",
                                       "....L---J.LJ.LJLJ..."]), 8)

    def test_ex4(self):
        return self.assertEqual(solve(["FF7FSF7F7F7F7F7F---7",
                                       "L|LJ||||||||||||F--J",
                                       "FL-7LJLJ||||||LJL-77",
                                       "F--JF--7||LJLJ7F7FJ-",
                                       "L---JF-JLJ.||-FJLJJ7",
                                       "|F|F-JF---7F7-L7L|7|",
                                       "|FFJF7L7F-JF7|JL---7",
                                       "7-L-JL7||F7|L7F-7F7|",
                                       "L.L7LFJ|||||FJL7||LJ",
                                       "L7JLJL-JLJLJL--JLJ.L"]), 10)

run(main)
