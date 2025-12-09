#!/usr/bin/env python3

#Advent of Code
#2025 Day 9, Part 2
#Solution by James C. (https://github.com/JamesMCo)

import os, sys
sys.path.append(os.path.abspath("../.."))
import unittest, util.read
from util.tests import run

from itertools import combinations
from shapely.geometry import Polygon

def solve(puzzle_input: list[str]) -> int:
    corner_tiles: list[tuple[int, int]] = [tuple(map(int, l.split(","))) for l in puzzle_input]
    red_and_green: Polygon = Polygon(corner_tiles)

    areas: dict[int, tuple[tuple[int, int], tuple[int, int]]] = {
        (max(a[0] + 1, b[0] + 1) - min(a[0], b[0])) * (max(a[1], b[1]) - min(a[1], b[1]) + 1): (a, b)
        for a, b in combinations(corner_tiles, 2)
    }

    for area in sorted(areas, reverse=True):
        area_polygon: Polygon = Polygon([
            (areas[area][0][0], areas[area][0][1]),
            (areas[area][0][0], areas[area][1][1]),
            (areas[area][1][0], areas[area][1][1]),
            (areas[area][1][0], areas[area][0][1])
        ])
        if not area_polygon.difference(red_and_green):
            return area

def main() -> tuple[str, int]:
    puzzle_input = util.read.as_lines()

    return "The largest area of any rectangle that can be made using only red and green tiles is {}.", solve(puzzle_input)

class AOC_Tests(unittest.TestCase):
    def test_ex1(self):
        return self.assertEqual(solve(["7,1",
                                       "11,1",
                                       "11,7",
                                       "9,7",
                                       "9,5",
                                       "2,5",
                                       "2,3",
                                       "7,3"]), 24)

if __name__ == "__main__":
    run(main)
