#!/usr/bin/env python3

#Advent of Code
#2021 Day 5, Part 2
#Solution by James C. (https://github.com/JamesMCo)

import os, sys
sys.path.append(os.path.abspath("../.."))
import unittest, util.read
from util.tests import run

from collections import defaultdict
import re

def solve(puzzle_input):
    vents = defaultdict(int)

    for line in puzzle_input:
        x1, y1, x2, y2 = [int(n) for n in re.match("(\d+),(\d+) -> (\d+),(\d+)", line).groups()]
        if x1 == x2:
            for y in range(min(y1, y2), max(y1, y2)+1):
                vents[(x1, y)] += 1
        elif y1 == y2:
            for x in range(min(x1, x2), max(x1, x2)+1):
                vents[(x, y1)] += 1
        else:
            # Always increase y, determine from this which way to change x
            points = sorted([(x1, y1), (x2, y2)], key=lambda p: p[1])
            x_dir = [-1, 1][points[0][0] < points[1][0]]
            y = points[0][1]
            for x in range(points[0][0], points[1][0]+x_dir, x_dir):
                vents[(x, y)] += 1
                y += 1

    return sum(1 for v in vents.values() if v > 1)

def main():
    puzzle_input = util.read.as_lines()

    overlaps = solve(puzzle_input)

    print("The number of points where at least two lines overlap is " + str(overlaps) + ".")

class AOC_Tests(unittest.TestCase):
    def test_ex1(self):
        return self.assertEqual(solve(["0,9 -> 5,9",
                                       "8,0 -> 0,8",
                                       "9,4 -> 3,4",
                                       "2,2 -> 2,1",
                                       "7,0 -> 7,4",
                                       "6,4 -> 2,0",
                                       "0,9 -> 2,9",
                                       "3,4 -> 1,4",
                                       "0,0 -> 8,8",
                                       "5,5 -> 8,2"]), 12)

run(main)
