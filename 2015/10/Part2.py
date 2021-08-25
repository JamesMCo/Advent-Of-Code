#!/usr/bin/env python3

#Advent of Code
#2015 Day 10, Part 2
#Solution by James C. (https://github.com/JamesMCo)

import os, sys
sys.path.append(os.path.abspath("../.."))
import unittest, util.read
from util.tests import run
import itertools

def solve(puzzle_input, repeats=50):
    current = puzzle_input
    for i in range(repeats):
        split = ["".join(grp) for num, grp in itertools.groupby(current)]
        new = ""
        for x in split:
            new += str(len(x))
            new += x[0]
        current = new
    return len(current)

def main():
    puzzle_input = util.read.as_string()

    length = solve(puzzle_input)

    print("The length of the final result is " + str(length) + ".")

class AOC_Tests(unittest.TestCase):
    @unittest.skip("No test cases")
    def test_ex1(self):
        pass

run(main)
