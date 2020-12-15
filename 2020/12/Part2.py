#!/usr/bin/env python3

#Advent of Code
#2020 Day 12, Part 2
#Solution by James C. (https://github.com/JamesMCo)

import os, sys
sys.path.append(os.path.abspath("../.."))
import unittest, util.read
from util.tests import run

from util.two_d_world import manhattan_distance

def solve(puzzle_input):
    ship_x,     ship_y     = (0, 0)
    waypoint_x, waypoint_y = (10, -1) 
    for movement in puzzle_input:
        action = movement[0]
        amount = int(movement[1:])

        if action == "N":
            waypoint_y -= amount
        elif action == "E":
            waypoint_x += amount
        elif action == "S":
            waypoint_y += amount
        elif action == "W":
            waypoint_x -= amount
        elif action == "F":
            ship_x += amount * waypoint_x
            ship_y += amount * waypoint_y
        elif (action == "R" and amount == 90) or (action == "L" and amount == 270):
            waypoint_x, waypoint_y = -waypoint_y, waypoint_x
        elif (action == "L" and amount == 90) or (action == "R" and amount == 270):
            waypoint_x, waypoint_y = waypoint_y, -waypoint_x
        elif (action == "L" or action == "R") and amount == 180:
            waypoint_x, waypoint_y = -waypoint_x, -waypoint_y

    return manhattan_distance(0, 0, ship_x, ship_y)

def main():
    puzzle_input = util.read.as_lines()

    distance = solve(puzzle_input)

    print("The distance betwen the start and end locations is " + str(distance) + ".")

class AOC_Tests(unittest.TestCase):
    def test_ex1(self):
        return self.assertEqual(solve(["F10", "N3", "F7", "R90", "F11"]), 286)

run(main)
