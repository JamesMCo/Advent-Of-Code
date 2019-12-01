#!/usr/bin/env python3

#Advent of Code
#2019 Day 1, Part 2
#Solution by James C. (https://github.com/JamesMCo)

import os, sys
sys.path.append(os.path.abspath("../.."))
import unittest, util.read
from util.tests import run

def solve(puzzle_input):
    def aux(n):
        s = int(n/3) - 2
        if s <= 0:
            return 0
        return s + aux(s)

    return sum(aux(x) for x in puzzle_input)

def main():
    puzzle_input = util.read.as_int_list("\n")

    fuel = solve(puzzle_input)

    print("The sum of the fuel requirements is " + str(fuel) + ".")

class AOC_Tests(unittest.TestCase):
    def test_ex1(self):
        self.assertEqual(solve([14]), 2)

    def test_ex2(self):
        self.assertEqual(solve([1969]), 966)

    def test_ex3(self):
        self.assertEqual(solve([100756]), 50346)

run(main)
