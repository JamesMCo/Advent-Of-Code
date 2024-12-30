#!/usr/bin/env python3

#Advent of Code
#2022 Day 18, Part 2
#Solution by James C. (https://github.com/JamesMCo)

import os, sys
sys.path.append(os.path.abspath("../.."))
import unittest, util.read
from util.tests import run

from math import inf

def solve(puzzle_input):
    cubes = set()
    external_air = set()

    min_x = min_y = min_z = inf
    max_x = max_y = max_z = -inf

    for line in puzzle_input:
        x, y, z = [int(x) for x in line.split(",")]
        cubes.add(tuple([x, y, z]))

        min_x = min(min_x, x-1)
        min_y = min(min_y, y-1)
        min_z = min(min_z, z-1)
        max_x = max(max_x, x+1)
        max_y = max(max_y, y+1)
        max_z = max(max_z, z+1)

    def neighbours(x, y, z):
        for offset in [(1,0,0), (-1,0,0), (0,1,0), (0,-1,0), (0,0,1), (0,0,-1)]:
            yield (x + offset[0], y + offset[1], z + offset[2])
    
    def in_bounds(cube):
        return (min_x <= cube[0] <= max_x) and (min_y <= cube[1] <= max_y) and (min_z <= cube[2] <= max_z)

    def is_trapped_air(cube):
        return cube not in cubes and not cube in external_air

    def count_external_sides(cube):
        return sum(not neighbour in cubes for neighbour in neighbours(*cube) if not is_trapped_air(neighbour))

    candidates = [(min_x, min_y, min_z)]
    while candidates:
        candidate = candidates.pop()
        external_air.add(candidate)

        for neighbour in neighbours(*candidate):
            if in_bounds(neighbour) and neighbour not in cubes and neighbour not in external_air:
                candidates.append(neighbour)

    return sum(count_external_sides(cube) for cube in cubes)

def main():
    puzzle_input = util.read.as_lines()

    sides = solve(puzzle_input)

    print("The surface area of the lava droplet is " + str(sides) + ".")

class AOC_Tests(unittest.TestCase):
    def test_ex1(self):
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
                                       "2,3,5"]), 58)

if __name__ == "__main__":
    run(main)
