#!/usr/bin/env python3

#Advent of Code
#2016 Day 1, Part 1
#Solution by James C. (https://github.com/JamesMCo)

import os, sys
sys.path.append(os.path.abspath("../.."))
import unittest, util.read
from util.tests import run

from math import fabs

def solve(puzzle_input):
    origin = (0, 0)
    here   = [0, 0]
    facing = 0 #N=0, E=1, S=2, W=3

    for i in puzzle_input:
        if i[0] == "L":
            facing -= 1
            if facing == -1: facing = 3
        else:
            facing += 1
            if facing == 4: facing = 0
        if facing == 0:
            here[1] += int(i[1:])
        elif facing == 1:
            here[0] += int(i[1:])
        elif facing == 2:
            here[1] -= int(i[1:])
        else:
            here[0] -= int(i[1:])

    dx = fabs(origin[0] - here[0])
    dy = fabs(origin[1] - here[1])
    return int(dx + dy)

def main():
    puzzle_input = util.read.as_string_list(", ")

    distance = solve(puzzle_input)

    print("The Easter Bunny HQ is " + str(distance) + " blocks away.")

class AOC_Tests(unittest.TestCase):
    def test_ex1(self):
        self.assertEqual(solve(["R2", "L3"]), 5)

    def test_ex2(self):
        self.assertEqual(solve(["R2", "R2", "R2"]), 2)

    def test_ex3(self):
        self.assertEqual(solve(["R5", "L5", "R5", "R3"]), 12)

run(main)
