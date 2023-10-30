#!/usr/bin/env python3

#Advent of Code
#2018 Day 23, Part 1
#Solution by James C. (https://github.com/JamesMCo)

import os, sys
sys.path.append(os.path.abspath("../.."))
import unittest, util.read
from util.tests import run

import re

def solve(puzzle_input):
    nanobot_description = re.compile = r"pos=<(-?\d+),(-?\d+),(-?\d+)>, r=(\d+)"
    class Nanobot:
        def __init__(self, description):
            data = re.match(nanobot_description, description)
            self.x, self.y, self.z = [int(a) for a in data.group(1, 2, 3)]
            self.radius  = int(data.group(4))

    def distance(a, b):
        return abs(a.x - b.x) + abs(a.y - b.y) + abs(a.z - b.z)

    nanobots = []
    largest = None
    for line in puzzle_input:
        nanobots.append(Nanobot(line))
        if largest == None or nanobots[-1].radius > largest.radius:
            largest = nanobots[-1]
    return sum([1 for nanobot in nanobots if distance(largest, nanobot) <= largest.radius])

def main():
    puzzle_input = util.read.as_lines()

    nanobots = solve(puzzle_input)

    print("The number of nanobots in range of the nanobot with the largest signal radius is " + str(nanobots) + ".")

class AOC_Tests(unittest.TestCase):
    def test_ex1(self):
        self.assertEqual(solve(["pos=<0,0,0>, r=4",
                                "pos=<1,0,0>, r=1",
                                "pos=<4,0,0>, r=3",
                                "pos=<0,2,0>, r=1",
                                "pos=<0,5,0>, r=3",
                                "pos=<0,0,3>, r=1",
                                "pos=<1,1,1>, r=1",
                                "pos=<1,1,2>, r=1",
                                "pos=<1,3,1>, r=1"]), 7)

run(main)
