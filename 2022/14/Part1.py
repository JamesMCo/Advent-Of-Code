#!/usr/bin/env python3

#Advent of Code
#2022 Day 14, Part 1
#Solution by James C. (https://github.com/JamesMCo)

import os, sys
sys.path.append(os.path.abspath("../.."))
import unittest, util.read
from util.tests import run

import re
from util.two_d_world import World

def solve(puzzle_input):
    cave_walls = {}
    for path in puzzle_input:
        path_coords = re.findall(r"(\d+),(\d+)", path)
        for (x1, y1), (x2, y2) in zip(path_coords, path_coords[1:]):
            x1, y1 = int(x1), int(y1)
            x2, y2 = int(x2), int(y2)

            if x1 == x2:
                for y in range(min(y1, y2), max(y1, y2) + 1):
                    cave_walls[(x1, y)] = "#"
            elif y1 == y2:
                for x in range(min(x1, x2), max(x1, x2) + 1):
                    cave_walls[(x, y1)] = "#"
    cave = World(".", True)
    cave.load_from_dict(cave_walls)
    cave.min_y = 0

    sand = 0
    while True:
        sand_x, sand_y = (500, 0)
        settled = False
        while True:
            if sand_y == cave.max_y:
                # Break without setting the settled flag, i.e. falling into the abyss
                break
            elif cave[(sand_x, sand_y+1)] == ".":
                sand_y += 1
                continue
            elif cave[(sand_x-1, sand_y+1)] == ".":
                sand_x -= 1
                sand_y += 1
                continue
            elif cave[(sand_x+1, sand_y+1)] == ".":
                sand_x += 1
                sand_y += 1
                continue
            else:
                cave[(sand_x, sand_y)] = "o"
                settled = True
                break
        if settled:
            sand += 1
        else:
            return sand

def main():
    puzzle_input = util.read.as_lines()

    sand = solve(puzzle_input)

    print("The number of units of sand that rest in the cave before falling into the abyss is " + str(sand) + ".")

class AOC_Tests(unittest.TestCase):
    def test_ex1(self):
        return self.assertEqual(solve(["498,4 -> 498,6 -> 496,6",
                                       "503,4 -> 502,4 -> 502,9 -> 494,9"]), 24)

run(main)
