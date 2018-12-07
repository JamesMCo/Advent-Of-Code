#!/usr/bin/env python3

#Advent of Code
#Day 11, Part 1
#Solution by James C. (https://github.com/JamesMCo)

import os, sys
sys.path.append(os.path.abspath("../.."))
import unittest
from util.tests import run

def solve(puzzle_input):
    x = 0
    y = 0

    directions_x = {"n":  0,
                    "ne": 1,
                    "se": 1,
                    "s":  0,
                    "sw": -1,
                    "nw": -1}
    directions_y = {"n":  -2,
                    "ne": -1,
                    "se": 1,
                    "s":  2,
                    "sw": 1,
                    "nw": -1}

    for direction in puzzle_input:
        x += directions_x[direction]
        y += directions_y[direction]

    path_x = 0
    path_y = 0
    steps = 0
    while (path_x, path_y) != (x, y):
        moved_x = 0
        if path_x < x:
            path_x += 1
            moved_x = 1
        elif path_x > x:
            path_x -= 1
            moved_x = 1
        if path_y < y:
            path_y += 1 + (1 - moved_x)
        elif path_y > y:
            path_y -= 1 + (1 - moved_x)
        steps += 1
    return steps

def main():
    f = open("puzzle_input.txt")
    puzzle_input = f.read()[:-1].split(",")
    f.close()

    steps = solve(puzzle_input)

    print("The fewest number of steps required to reach the child process is " + str(steps) + ".")

class AOC_Tests(unittest.TestCase):
    def test_ex1(self):
        self.assertEqual(solve(["ne", "ne", "ne"]), 3)

    def test_ex2(self):
        self.assertEqual(solve(["ne", "ne", "sw", "sw"]), 0)

    def test_ex3(self):
        self.assertEqual(solve(["ne", "ne", "s", "s"]), 2)

    def test_ex4(self):
        self.assertEqual(solve(["se", "sw", "se", "sw", "sw"]), 3)

run(main)
