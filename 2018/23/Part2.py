#!/usr/bin/env python3

#Advent of Code
#2018 Day 23, Part 2
#Solution by James C. (https://github.com/JamesMCo)

import os, sys
sys.path.append(os.path.abspath("../.."))
import unittest, util.read
from util.tests import run

import re
import z3

def solve(puzzle_input):
    def z3_abs(n):
        return z3.If(n >= 0, n, -n)

    class Nanobot:
        nanobot_description = re.compile(r"pos=<(-?\d+),(-?\d+),(-?\d+)>, r=(\d+)")

        def __init__(self, description):
            data = self.nanobot_description.match(description)
            self.x, self.y, self.z = [int(a) for a in data.group(1, 2, 3)]
            self.radius  = int(data.group(4))

        def z3_constraint(self, x, y, z):
            return z3.If(z3_abs(x - self.x) + z3_abs(y - self.y) + z3_abs(z - self.z) <= self.radius, 1, 0)

    # Solution heavily based on this comment/solution by /u/mserrano
    # https://www.reddit.com/r/adventofcode/comments/a8s17l/comment/ecdbux2
    # I also just used z3 for the first time today (solving 2023 Day 24 Part 2).
    # My first attempt using z3 didn't use an Optimize object, which it turns out is
    # quite a useful tool for this puzzle!
    # Task for future me: learn more about z3 and its API and how to make use of it!

    nanobots = [Nanobot(line) for line in puzzle_input]
    optimiser = z3.Optimize()

    # Inputs
    x, y, z = z3.Ints("x y z")
    in_radius = [z3.Int(f"in_radius_{i}") for i in range(len(puzzle_input))]

    # Outputs
    number_of_nanobots = z3.Int("number_of_nanobots")
    distance = z3.Int("distance")

    # For each nanobot, add a constraint for the (x, y, z) to be in the range of the nanobot
    # and also keep track of whether the constraint is met
    optimiser.add([in_radius[i] == nanobot.z3_constraint(x, y, z) for i, nanobot in enumerate(nanobots)])

    # Add a constraint for the number of nanobots that see the (x, y, z) coordinate
    optimiser.add(number_of_nanobots == sum(in_radius))
    # Add a constraint for the manhattan distance from the origin
    optimiser.add(distance == z3_abs(x) + z3_abs(y) + z3_abs(z))

    # Try to maximise the number of nanobots, and try to minimise the distance from the origin
    optimiser.maximize(number_of_nanobots)
    optimiser.minimize(distance)

    optimiser.check()
    return optimiser.model()[distance]

def main():
    puzzle_input = util.read.as_lines()

    nanobots = solve(puzzle_input)

    print("The number of nanobots in range of the nanobot with the largest signal radius is " + str(nanobots) + ".")

class AOC_Tests(unittest.TestCase):
    def test_ex1(self):
        self.assertEqual(solve(["pos=<10,12,12>, r=2",
                                "pos=<12,14,12>, r=2",
                                "pos=<16,12,12>, r=4",
                                "pos=<14,14,14>, r=6",
                                "pos=<50,50,50>, r=200",
                                "pos=<10,10,10>, r=5"]), 36)

run(main)
