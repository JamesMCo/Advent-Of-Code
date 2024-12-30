#!/usr/bin/env python3

#Advent of Code
#2018 Day 18, Part 1
#Solution by James C. (https://github.com/JamesMCo)

import os, sys
sys.path.append(os.path.abspath("../.."))
import unittest, util.read
from util.tests import run

def solve(puzzle_input):
    prev_area = puzzle_input[:]
    area = []
    for minute in range(10):
        area = []
        for y, row in enumerate(prev_area):
            area.append("")
            for x, col in enumerate(row):
                neighbours = [prev_area[y_offset][x_offset]
                              for x_offset in range(x-1,x+2)
                              for y_offset in range(y-1,y+2)
                              if  (x_offset, y_offset) != (x, y)
                              and 0 <= x_offset < len(prev_area[0])
                              and 0 <= y_offset < len(prev_area)]
                if col == "." and neighbours.count("|") >= 3:
                    area[-1] += "|"
                elif col == "|" and neighbours.count("#") >= 3:
                    area[-1] += "#"
                elif col == "#" and (neighbours.count("#") == 0 or neighbours.count("|") == 0):
                    area[-1] += "."
                else:
                    area[-1] += col
        prev_area = area[:]

    area = "".join(area)
    return area.count("|") * area.count("#")

def main():
    puzzle_input = util.read.as_lines()

    resource_value = solve(puzzle_input)

    print("The total resource value of the collection area after 10 minutes is " + str(resource_value) + ".")

class AOC_Tests(unittest.TestCase):
    def test_ex1(self):
        self.assertEqual(solve([".#.#...|#.",
                                ".....#|##|",
                                ".|..|...#.",
                                "..|#.....#",
                                "#.#|||#|#|",
                                "...#.||...",
                                ".|....|...",
                                "||...#|.#|",
                                "|.||||..|.",
                                "...#.|..|."]), 1147)

if __name__ == "__main__":
    run(main)
