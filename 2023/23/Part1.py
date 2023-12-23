#!/usr/bin/env python3

#Advent of Code
#2023 Day 23, Part 1
#Solution by James C. (https://github.com/JamesMCo)

import os, sys
sys.path.append(os.path.abspath("../.."))
import unittest, util.read
from util.tests import run

from collections import deque

def solve(puzzle_input: list[str]) -> int:
    width = len(puzzle_input[0])
    height = len(puzzle_input)

    start = (puzzle_input[0].index("."), 0, )
    target = (puzzle_input[-1].index("."), height - 1)

    def neighbours(x: int, y: int) -> set[tuple[int, int]]:
        output: set[tuple[int, int]] = set()
        match puzzle_input[y][x]:
            case "^":
                if 0 <= x < width and 0 <= y - 1 < height and puzzle_input[y - 1][x] in ".^<>":
                    output.add((x, y - 1))
            case ">":
                if 0 <= x + 1 < width and 0 <= y < height and puzzle_input[y][x + 1] in ".>^v":
                    output.add((x + 1, y))
            case "v":
                if 0 <= x < width and 0 <= y + 1 < height and puzzle_input[y + 1][x] in ".v<>":
                    output.add((x, y + 1))
            case "<":
                if 0 <= x - 1 < width and 0 <= y < height and puzzle_input[y][x - 1] in ".<^v":
                    output.add((x - 1, y))
            case ".":
                for dx, dy, allowed_cells in ((0, -1, ".^<>"), (1, 0, ".>^v"), (0, 1, ".v<>"), (-1, 0, ".<^v")):
                    if 0 <= x + dx < width and 0 <= y + dy < height and puzzle_input[y + dy][x + dx] in allowed_cells:
                        output.add((x + dx, y + dy))
        return output

    queue: deque[tuple[tuple[int, int], set[tuple[int, int]]]] = deque()
    queue.append((start, set()))
    longest_length = 0

    while queue:
        from_coord, seen = queue.popleft()
        while True:
            if from_coord == target:
                longest_length = max(longest_length, len(seen))
                break

            next_cells = neighbours(*from_coord) - seen
            if len(next_cells) == 1:
                # If only one option, skip immediately to consider it
                # Means that we will only extend the queue at junctions
                seen |= {from_coord}
                (from_coord,) = next_cells
            else:
                queue.extend((next_cell, seen | {from_coord}) for next_cell in next_cells)
                break

    return longest_length

def main() -> tuple[str, int]:
    puzzle_input = util.read.as_lines()

    return "The longest hike is {} steps long.", solve(puzzle_input)

class AOC_Tests(unittest.TestCase):
    def test_ex1(self):
        return self.assertEqual(solve(["#.#####################",
                                       "#.......#########...###",
                                       "#######.#########.#.###",
                                       "###.....#.>.>.###.#.###",
                                       "###v#####.#v#.###.#.###",
                                       "###.>...#.#.#.....#...#",
                                       "###v###.#.#.#########.#",
                                       "###...#.#.#.......#...#",
                                       "#####.#.#.#######.#.###",
                                       "#.....#.#.#.......#...#",
                                       "#.#####.#.#.#########v#",
                                       "#.#...#...#...###...>.#",
                                       "#.#.#v#######v###.###v#",
                                       "#...#.>.#...>.>.#.###.#",
                                       "#####v#.#.###v#.#.###.#",
                                       "#.....#...#...#.#.#...#",
                                       "#.#########.###.#.#.###",
                                       "#...###...#...#...#.###",
                                       "###.###.#.###v#####v###",
                                       "#...#...#.#.>.>.#.>.###",
                                       "#.###.###.#.###.#.#v###",
                                       "#.....###...###...#...#",
                                       "#####################.#"]), 94)

run(main)
