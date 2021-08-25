#!/usr/bin/env python3

#Advent of Code
#2015 Day 10, Part 1
#Solution by James C. (https://github.com/JamesMCo)

import os, sys
sys.path.append(os.path.abspath("../.."))
import unittest, util.read
from util.tests import run
import itertools

def solve(puzzle_input, repeats=40):
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
    def test_ex1(self):
        return self.assertEqual(solve("1", 1), 2)

    def test_ex2(self):
        return self.assertEqual(solve("11", 1), 2)

    def test_ex3(self):
        return self.assertEqual(solve("21", 1), 4)

    def test_ex4(self):
        return self.assertEqual(solve("1211", 1), 6)

    def test_ex5(self):
        return self.assertEqual(solve("111221", 1), 6)

run(main)
