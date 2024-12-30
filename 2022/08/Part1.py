#!/usr/bin/env python3

#Advent of Code
#2022 Day 8, Part 1
#Solution by James C. (https://github.com/JamesMCo)

import os, sys
sys.path.append(os.path.abspath("../.."))
import unittest, util.read
from util.tests import run

def solve(puzzle_input):
    puzzle_input = [[int(col) for col in row] for row in puzzle_input]
    width  = len(puzzle_input[0])
    height = len(puzzle_input)

    def visible(x, y):
        if x in [0, width - 1] or y in [0, height - 1]:
            return True
        elif puzzle_input[y][x] > max(puzzle_input[y][:x]):
            # Row, left to right
            return True
        elif puzzle_input[y][x] > max(puzzle_input[y][x+1:]):
            # Row, right to left
            return True
        elif puzzle_input[y][x] > max(row[x] for row in puzzle_input[:y]):
            # Col, top to bottom
            return True
        elif puzzle_input[y][x] > max(row[x] for row in puzzle_input[y+1:]):
            # Col, bottom to top
            return True
        else:
            return False

    return sum(visible(x, y) for x in range(width) for y in range(height))

def main():
    puzzle_input = util.read.as_lines()

    trees = solve(puzzle_input)

    print("The number of trees visible from outside the grid is " + str(trees) + ".")

class AOC_Tests(unittest.TestCase):
    def test_ex1(self):
        return self.assertEqual(solve(["30373",
                                       "25512",
                                       "65332",
                                       "33549",
                                       "35390"]), 21)

if __name__ == "__main__":
    run(main)
