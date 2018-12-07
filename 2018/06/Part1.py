#!/usr/bin/env python3

#Advent of Code
#Day 6, Part 1
#Solution by James C. (https://github.com/JamesMCo)

import os, sys, colorama, time
sys.path.append(os.path.abspath("../.."))
import unittest, util.read
from util.tests import run

from collections import defaultdict

def solve(puzzle_input):
    def distance(a, b):
        return abs(a[0]-b[0]) + abs(a[1]-b[1])

    puzzle_input = [(int(x.split(", ")[0]), int(x.split(", ")[1])) for x in puzzle_input]
    width  = max([x[0] for x in puzzle_input]) - min([x[0] for x in puzzle_input])
    height = max([x[1] for x in puzzle_input]) - min([x[1] for x in puzzle_input])

    left  = min([z[0] for z in puzzle_input]) - 10
    right = min([z[0] for z in puzzle_input]) + width + 10
    top   = min([z[1] for z in puzzle_input]) - 10
    bot   = min([z[1] for z in puzzle_input]) + height + 10
    grid = defaultdict(int)

    #Distances for the grid, with a margin of 10 on all sides
    for x in range(left, right+1):
        for y in range(top, bot+1):
            working = sorted([(z, distance(z, (x, y))) for z in puzzle_input], key=lambda a: a[1])
            if [z[1] for z in working].count(working[0][1]) == 1:
                grid[str(working[0][0])] += 1

    #Discount areas that are infinite (closest to the borders)
    for x in range(left, right+1):
        for y in range(top, bot+1):
            if y not in [top, bot] and x not in [left, right]:
                continue

            working = sorted([(z, distance(z, (x, y))) for z in puzzle_input], key=lambda a: a[1])
            if [z[1] for z in working].count(working[0][1]) == 1:
                grid[str(working[0][0])] = 0

    return max(grid.values())

def main():
    puzzle_input = util.read.as_lines()

    area = solve(puzzle_input)

    print("The size of the largest (non infinite) area is " + str(area) + ".")

class AOC_Tests(unittest.TestCase):
    def test_ex1(self):
        self.assertEqual(solve(["1, 1",
                                "1, 6",
                                "8, 3",
                                "3, 4",
                                "5, 5",
                                "8, 9"]), 17)

run(main)
