#!/usr/bin/env python3

#Advent of Code
#2024 Day 18, Part 1
#Solution by James C. (https://github.com/JamesMCo)

import os, sys
sys.path.append(os.path.abspath("../.."))
import unittest, util.read
from util.tests import run

from collections import deque

def solve(puzzle_input: list[str], width: int = 71, byte_cutoff: int = 1024) -> int:
    corrupted: set[tuple[int, int]] = set()
    for corrupted_from, corrupted_loc_str in enumerate(puzzle_input[:byte_cutoff]):
        corrupted_loc: tuple[int, int] = tuple(int(n) for n in corrupted_loc_str.split(","))
        if corrupted_loc not in corrupted:
            corrupted.add(corrupted_loc)

    queue: deque[tuple[tuple[int, int], set[tuple[int, int]]]] = deque([((0, 0), set())])
    seen: set[tuple[int, int]] = set([(0, 0)])
    while queue:
        current_loc: tuple[int, int]
        current_visited: set[tuple[int, int]]
        current_loc, current_visited = queue.popleft()

        if current_loc == (width - 1, width - 1):
            return len(current_visited)
        else:
            for neighbour_loc in [
                (current_loc[0], current_loc[1] - 1),
                (current_loc[0] - 1, current_loc[1]),
                (current_loc[0], current_loc[1] + 1),
                (current_loc[0] + 1, current_loc[1])
            ]:
                if neighbour_loc[0] < 0 or neighbour_loc[0] >= width:
                    continue
                elif neighbour_loc[1] < 0 or neighbour_loc[1] >= width:
                    continue
                elif neighbour_loc in corrupted:
                    continue
                elif neighbour_loc in seen:
                    continue
                seen.add(neighbour_loc)
                queue.append((neighbour_loc, current_visited | {current_loc}))

def main() -> tuple[str, int]:
    puzzle_input = util.read.as_lines()

    return "The minimum number of steps needed to reach the exit is {}.", solve(puzzle_input)

class AOC_Tests(unittest.TestCase):
    def test_ex1(self):
        return self.assertEqual(solve(["5,4",
                                       "4,2",
                                       "4,5",
                                       "3,0",
                                       "2,1",
                                       "6,3",
                                       "2,4",
                                       "1,5",
                                       "0,6",
                                       "3,3",
                                       "2,6",
                                       "5,1",
                                       "1,2",
                                       "5,5",
                                       "2,5",
                                       "6,5",
                                       "1,4",
                                       "0,4",
                                       "6,4",
                                       "1,1",
                                       "6,1",
                                       "1,0",
                                       "0,5",
                                       "1,6",
                                       "2,0"], 7, 12), 22)

run(main)
