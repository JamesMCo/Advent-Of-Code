#!/usr/bin/env python3

#Advent of Code
#2020 Day 12, Part 1
#Solution by James C. (https://github.com/JamesMCo)

import os, sys
sys.path.append(os.path.abspath("../.."))
import unittest, util.read
from util.tests import run

from util.two_d_world import manhattan_distance

def solve(puzzle_input):
    # North = 0, East = 90, South = 180, West = 270
    facing = 90
    x, y = (0, 0)
    for movement in puzzle_input:
        action = movement[0]
        amount = int(movement[1:])

        if action == "N" or (action == "F" and facing == 0):
            y -= amount
        elif action == "E" or (action == "F" and facing == 90):
            x += amount
        elif action == "S" or (action == "F" and facing == 180):
            y += amount
        elif action == "W" or (action == "F" and facing == 270):
            x -= amount
        elif action == "R":
            facing = (facing + amount) % 360
        elif action == "L":
            facing = (facing - amount) % 360

    return manhattan_distance(0, 0, x, y)

def main():
    puzzle_input = util.read.as_lines()

    distance = solve(puzzle_input)

    print("The distance betwen the start and end locations is " + str(distance) + ".")

class AOC_Tests(unittest.TestCase):
    def test_ex1(self):
        return self.assertEqual(solve(["F10", "N3", "F7", "R90", "F11"]), 25)

run(main)
