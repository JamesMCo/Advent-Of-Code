#!/usr/bin/env python3

#Advent of Code
#2019 Day 1, Part 1
#Solution by James C. (https://github.com/JamesMCo)

import os, sys
sys.path.append(os.path.abspath("../.."))
import unittest, util.read
from util.tests import run

def solve(puzzle_input):
    return sum(int(x/3) - 2 for x in puzzle_input)

def main():
    puzzle_input = util.read.as_int_list("\n")

    fuel = solve(puzzle_input)

    print("The sum of the fuel requirements is " + str(fuel) + ".")

class AOC_Tests(unittest.TestCase):
    def test_ex1(self):
        self.assertEqual(solve([12]), 2)

    def test_ex2(self):
        self.assertEqual(solve([14]), 2)

    def test_ex3(self):
        self.assertEqual(solve([1969]), 654)

    def test_ex4(self):
        self.assertEqual(solve([100756]), 33583)

if __name__ == "__main__":
    run(main)
