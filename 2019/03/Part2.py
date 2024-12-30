#!/usr/bin/env python3

#Advent of Code
#2019 Day 3, Part 2
#Solution by James C. (https://github.com/JamesMCo)

import os, sys
sys.path.append(os.path.abspath("../.."))
import unittest, util.read
from util.tests import run

from collections import defaultdict

def solve(puzzle_input):
    def step(coords, direction):
        if direction   == "U":
            return (coords[0], coords[1] + 1)
        elif direction == "D":
            return (coords[0], coords[1] - 1)
        elif direction == "R":
            return (coords[0] + 1, coords[1])
        elif direction == "L":
            return (coords[0] - 1, coords[1])

    a = [(x[0], int(x[1:])) for x in puzzle_input[0].split(",")]
    b = [(x[0], int(x[1:])) for x in puzzle_input[1].split(",")]
    panel   = defaultdict(int)
    steps_a = defaultdict(int)
    steps_b = defaultdict(int)

    coords = (0, 0)
    steps  = 0
    for direction, distance in a:
        for i in range(distance):
            coords = step(coords, direction)
            steps += 1

            panel[coords] = 1
            if steps_a[coords] == 0:
                steps_a[coords] = steps

    coords = (0, 0)
    steps  = 0
    for direction, distance in b:
        for i in range(distance):
            coords = step(coords, direction)
            steps += 1

            if panel[coords] == 1:
                panel[coords] = 2
            if steps_b[coords] == 0:
                steps_b[coords] = steps

    crossed = sorted([c for c in panel.keys() if panel[c] == 2 and c != (0, 0)],
                      key=lambda x: steps_a[x] + steps_b[x])

    return steps_a[crossed[0]] + steps_b[crossed[0]]

def main():
    puzzle_input = util.read.as_lines()

    steps = solve(puzzle_input)

    print("The fewest combined steps to reach an intersection is " + str(steps) + ".")

class AOC_Tests(unittest.TestCase):
    def test_ex1(self):
        self.assertEqual(solve(["R8,U5,L5,D3",
                                "U7,R6,D4,L4"]), 30)

    def test_ex2(self):
        self.assertEqual(solve(["R75,D30,R83,U83,L12,D49,R71,U7,L72",
                                "U62,R66,U55,R34,D71,R55,D58,R83"]), 610)
    
    def test_ex3(self):
        self.assertEqual(solve(["R98,U47,R26,D63,R33,U87,L62,D20,R33,U53,R51",
                                "U98,R91,D20,R16,D67,R40,U7,R15,U6,R7"]), 410)

if __name__ == "__main__":
    run(main)
