#!/usr/bin/env python3

#Advent of Code
#2016 Day 3, Part 1
#Solution by James C. (https://github.com/JamesMCo)

import os, sys
sys.path.append(os.path.abspath("../.."))
import unittest, util.read
from util.tests import run

def solve(puzzle_input):
    possible = 0

    for t in puzzle_input:
        if t == "": continue
        values = t.split(" ")
        sides = []
        for v in values:
            if v != "":
                sides.append(v)
        if (int(sides[0]) + int(sides[1]) > int(sides[2]) and
            int(sides[1]) + int(sides[2]) > int(sides[0]) and
            int(sides[2]) + int(sides[0]) > int(sides[1])):
            possible += 1

    return possible

def main():
    puzzle_input = util.read.as_lines()

    possible = solve(puzzle_input)

    print("There are " + str(possible) + " possible triangles.")

class AOC_Tests(unittest.TestCase):
    @unittest.skip("No test cases")
    def test_ex1(self):
        pass

if __name__ == "__main__":
    run(main)
