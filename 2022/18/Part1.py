#!/usr/bin/env python3

#Advent of Code
#2022 Day 18, Part 1
#Solution by James C. (https://github.com/JamesMCo)

import os, sys
sys.path.append(os.path.abspath("../.."))
import unittest, util.read
from util.tests import run

def solve(puzzle_input):
    cubes = set()
    for line in puzzle_input:
        cubes.add(tuple([int(x) for x in line.split(",")]))
    
    def neighbours(x, y, z):
        for offset in [(1,0,0), (-1,0,0), (0,1,0), (0,-1,0), (0,0,1), (0,0,-1)]:
            yield (x + offset[0], y + offset[1], z + offset[2])

    return sum(sum(not neighbour in cubes for neighbour in neighbours(*cube)) for cube in cubes)

def main():
    puzzle_input = util.read.as_lines()

    sides = solve(puzzle_input)

    print("The surface area of the lava droplet is " + str(sides) + ".")

class AOC_Tests(unittest.TestCase):
    def test_ex1(self):
        return self.assertEqual(solve(["1,1,1",
                                       "2,1,1"]), 10)

    def test_ex2(self):
        return self.assertEqual(solve(["2,2,2",
                                       "1,2,2",
                                       "3,2,2",
                                       "2,1,2",
                                       "2,3,2",
                                       "2,2,1",
                                       "2,2,3",
                                       "2,2,4",
                                       "2,2,6",
                                       "1,2,5",
                                       "3,2,5",
                                       "2,1,5",
                                       "2,3,5"]), 64)

run(main)
