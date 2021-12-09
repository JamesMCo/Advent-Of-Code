#!/usr/bin/env python3

#Advent of Code
#2021 Day 9, Part 2
#Solution by James C. (https://github.com/JamesMCo)

import os, sys
sys.path.append(os.path.abspath("../.."))
import unittest, util.read
from util.tests import run

from collections import defaultdict
from functools import cache
from math import prod

def solve(puzzle_input):
    for i in range(len(puzzle_input)):
        puzzle_input[i] = [int(x) for x in puzzle_input[i]]

    def neighbours(x, y):
        coords = [(x+dx, y+dy) for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)] if 0 <= (x+dx) < len(puzzle_input[i]) and 0 <= (y+dy) < len(puzzle_input)]
        for (nx, ny) in coords:
            yield nx, ny, puzzle_input[ny][nx]

    @cache
    def find_basin_low_point(x, y):
        if all(puzzle_input[y][x] < nv for nx, ny, nv in neighbours(x, y)):
            return (x, y)
        elif puzzle_input[y][x] != 9:
            for nx, ny, nv in neighbours(x, y):
                if nv < puzzle_input[y][x]:
                    return find_basin_low_point(nx, ny)
        return None

    basins = defaultdict(int)
    for y in range(len(puzzle_input)):
        for x in range(len(puzzle_input[y])):
            if (low_point := find_basin_low_point(x, y)):
                basins[low_point] += 1
    
    return prod(sorted(basins.values())[-3:])

def main():
    puzzle_input = util.read.as_lines()

    basins = solve(puzzle_input)

    print("The product of the sizes of the three largest basins is " + str(basins) + ".")

class AOC_Tests(unittest.TestCase):
    def test_ex1(self):
        return self.assertEqual(solve(["2199943210",
                                       "3987894921",
                                       "9856789892",
                                       "8767896789",
                                       "9899965678"]), 1134)

run(main)
