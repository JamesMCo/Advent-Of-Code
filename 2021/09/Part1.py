#!/usr/bin/env python3

#Advent of Code
#2021 Day 9, Part 1
#Solution by James C. (https://github.com/JamesMCo)

import os, sys
sys.path.append(os.path.abspath("../.."))
import unittest, util.read
from util.tests import run

def solve(puzzle_input):
    for i in range(len(puzzle_input)):
        puzzle_input[i] = [int(x) for x in puzzle_input[i]]

    def neighbours(x, y):
        coords = [(x+dx, y+dy) for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)] if 0 <= (x+dx) < len(puzzle_input[i]) and 0 <= (y+dy) < len(puzzle_input)]
        for (nx, ny) in coords:
            yield puzzle_input[ny][nx]

    return sum(puzzle_input[y][x]+1 for y in range(len(puzzle_input)) for x in range(len(puzzle_input[y])) if all(puzzle_input[y][x] < neighbour for neighbour in neighbours(x, y)))

def main():
    puzzle_input = util.read.as_lines()

    risk_levels = solve(puzzle_input)

    print("The sum of the risk levels of all low points on the heightmap is " + str(risk_levels) + ".")

class AOC_Tests(unittest.TestCase):
    def test_ex1(self):
        return self.assertEqual(solve(["2199943210",
                                       "3987894921",
                                       "9856789892",
                                       "8767896789",
                                       "9899965678"]), 15)

run(main)
