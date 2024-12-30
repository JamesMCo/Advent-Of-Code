#!/usr/bin/env python3

#Advent of Code
#2020 Day 17, Part 1
#Solution by James C. (https://github.com/JamesMCo)

import os, sys
sys.path.append(os.path.abspath("../.."))
import unittest, util.read
from util.tests import run

import collections
from functools import cache

def solve(puzzle_input):
    world = collections.defaultdict(lambda: ".")
    for y, row in enumerate(puzzle_input):
        for x, col in enumerate(row):
            world[(x, y, 0)] = col
    min_x = min_y = min_z = -1
    max_x = len(puzzle_input[0])
    max_y = len(puzzle_input)
    max_z = 1

    @cache
    def neighbours(x, y, z):
        return [(dx, dy, dz) for dx in range(x - 1, x + 2) for dy in range(y - 1, y + 2) for dz in range(z - 1, z + 2) if not (dx == x and dy == y and dz == z)]

    def step(prev):
        new = collections.defaultdict(lambda: ".")
        for x in range(min_x, max_x + 1):
            for y in range(min_y, max_y + 1):
                for z in range(min_z, max_z + 1):
                    active_neighbours = sum(1 for nx, ny, nz in neighbours(x, y, z) if prev[(nx, ny, nz)] == "#")
                    if prev[(x, y, z)] == "#" and active_neighbours not in [2, 3]:
                        new[(x, y, z)] = "."
                    elif prev[(x, y, z)] == "." and active_neighbours == 3:
                        new[(x, y, z)] = "#"
                    else:
                        new[(x, y, z)] = prev[(x, y, z)]
        return new

    for i in range(6):
        world = step(world)

        min_x -= 1
        min_y -= 1
        min_z -= 1
        
        max_x += 1
        max_y += 1
        max_z += 1
    return sum(1 for cube in world.values() if cube == "#")

def main():
    puzzle_input = util.read.as_lines()

    active = solve(puzzle_input)

    print("The number of active cubes is " + str(active) + ".")

class AOC_Tests(unittest.TestCase):
    def test_ex1(self):
        return self.assertEqual(solve([".#.",
                                       "..#",
                                       "###"]), 112)

if __name__ == "__main__":
    run(main)
