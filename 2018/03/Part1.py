#!/usr/bin/env python3

#Advent of Code
#Day 3, Part 1
#Solution by James C. (https://github.com/JamesMCo)

import os, sys, colorama, time
sys.path.append(os.path.abspath("../.."))
import unittest
from util.tests import run

from collections import defaultdict

def solve(puzzle_input):
    fabric = defaultdict(int)

    for line in puzzle_input:
        left, top     = [int(x) for x in line.split()[2][:-1].split(",")]
        width, height = [int(x) for x in line.split()[3].split("x")]

        for x in range(left, left+width):
            for y in range(top, top+height):
                fabric[f"{x},{y}"] += 1

    count = 0
    for val in fabric.values():
        if val > 1:
            count += 1
    return count

def main():
    f = open("puzzle_input.txt")
    puzzle_input = f.read().strip().split("\n")
    f.close()

    inches = solve(puzzle_input)

    print("The number of overlapping square inches is " + str(inches) + ".")

class AOC_Tests(unittest.TestCase):
    def test_ex1(self):
        self.assertEqual(solve(["#1 @ 1,3: 4x4",
                                "#2 @ 3,1: 4x4",
                                "#3 @ 5,5: 2x2"]), 4)

run(main)
