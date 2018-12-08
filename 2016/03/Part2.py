#!/usr/bin/env python3

#Advent of Code
#2016 Day 3, Part 2
#Solution by James C. (https://github.com/JamesMCo)

import os, sys
sys.path.append(os.path.abspath("../.."))
import unittest, util.read
from util.tests import run

def solve(puzzle_input):
    possible = 0
    column1, column2, column3 = [], [], []

    for t in puzzle_input:
        if t == "": continue
        values = t.split(" ")
        sides = []
        for v in values:
            if v != "":
                sides.append(v)
        column1.append(str(sides[0]).zfill(3))
        column2.append(str(sides[1]).zfill(3))
        column3.append(str(sides[2]).zfill(3))

    for i in range(0, len(column1), 3):
        a, b, c = column1[i:i + 3]
        if (int(a) + int(b) > int(c) and
            int(b) + int(c) > int(a) and
            int(c) + int(a) > int(b)):
            possible += 1
        a, b, c = column2[i:i + 3]
        if (int(a) + int(b) > int(c) and
            int(b) + int(c) > int(a) and
            int(c) + int(a) > int(b)):
            possible += 1
        a, b, c = column3[i:i + 3]
        if (int(a) + int(b) > int(c) and
            int(b) + int(c) > int(a) and
            int(c) + int(a) > int(b)):
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

run(main)
