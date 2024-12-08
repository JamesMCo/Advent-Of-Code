#!/usr/bin/env python3

#Advent of Code
#2024 Day 8, Part 1
#Solution by James C. (https://github.com/JamesMCo)

import os, sys
sys.path.append(os.path.abspath("../.."))
import unittest, util.read
from util.tests import run

from collections import defaultdict
from util.two_d_world import World

def solve(puzzle_input: list[str]) -> int:
    area: World = World(".")
    area.load_from_lists(puzzle_input)

    antennas: defaultdict[str, list[tuple[int, int]]] = defaultdict(list)
    antinodes: set[tuple[int, int]] = set()

    for y in range(area.min_y, area.max_y + 1):
        for x in range(area.min_x, area.max_x + 1):
            frequency: str
            if (frequency := area[(x, y)]) != ".":
                other: tuple[int, int]
                for other in antennas[frequency]:
                    # dx and dy from other to current antenna
                    dx = x - other[0]
                    dy = y - other[1]
                    if dx == int(dx) and dy == int(dy):
                        if area.in_bounds(other[0] - dx, other[1] - dy):
                            antinodes.add((other[0] - dx, other[1] - dy))
                        if area.in_bounds(x + dx, y + dy):
                            antinodes.add((x + dx, y + dy))

                antennas[frequency].append((x, y))

    return len(antinodes)

def main() -> tuple[str, int]:
    puzzle_input = util.read.as_lines()

    return "The number of unique locations that contain an antinode is {}.", solve(puzzle_input)

class AOC_Tests(unittest.TestCase):
    def test_ex1(self):
        return self.assertEqual(solve(["..........",
                                       "..........",
                                       "..........",
                                       "....a.....",
                                       "..........",
                                       ".....a....",
                                       "..........",
                                       "..........",
                                       "..........",
                                       ".........."]), 2)

    def test_ex2(self):
        return self.assertEqual(solve(["..........",
                                       "..........",
                                       "..........",
                                       "....a.....",
                                       "........a.",
                                       ".....a....",
                                       "..........",
                                       "..........",
                                       "..........",
                                       ".........."]), 4)

    def test_ex3(self):
        return self.assertEqual(solve(["..........",
                                       "..........",
                                       "..........",
                                       "....a.....",
                                       "........a.",
                                       ".....a....",
                                       "..........",
                                       "......A...",
                                       "..........",
                                       ".........."]), 4)

    def test_ex4(self):
        return self.assertEqual(solve(["............",
                                       "........0...",
                                       ".....0......",
                                       ".......0....",
                                       "....0.......",
                                       "......A.....",
                                       "............",
                                       "............",
                                       "........A...",
                                       ".........A..",
                                       "............",
                                       "............"]), 14)

run(main)
