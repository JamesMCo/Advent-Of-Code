#!/usr/bin/env python3

#Advent of Code
#2022 Day 8, Part 2
#Solution by James C. (https://github.com/JamesMCo)

import os, sys
sys.path.append(os.path.abspath("../.."))
import unittest, util.read
from util.tests import run

def solve(puzzle_input):
    puzzle_input = [[int(col) for col in row] for row in puzzle_input]
    width  = len(puzzle_input[0])
    height = len(puzzle_input)

    def scenic_score(x, y):
        up, down, left, right = 0, 0, 0, 0

        if y != 0:
            up = 1
            while y - up != 0 and puzzle_input[y-up][x] < puzzle_input[y][x]:
                up += 1
        if y != height - 1:
            down = 1
            while y + down != height - 1 and puzzle_input[y+down][x] < puzzle_input[y][x]:
                down += 1
        if x != 0:
            left = 1
            while x - left != 0 and puzzle_input[y][x-left] < puzzle_input[y][x]:
                left += 1
        if x != width - 1:
            right = 1
            while x + right != width - 1 and puzzle_input[y][x+right] < puzzle_input[y][x]:
                right += 1

        return up * down * left * right

    return max(scenic_score(x, y) for x in range(width) for y in range(height))

def main():
    puzzle_input = util.read.as_lines()

    score = solve(puzzle_input)

    print("The highest scenic score for any tree is " + str(score) + ".")

class AOC_Tests(unittest.TestCase):
    def test_ex1(self):
        return self.assertEqual(solve(["30373",
                                       "25512",
                                       "65332",
                                       "33549",
                                       "35390"]), 8)

run(main)
