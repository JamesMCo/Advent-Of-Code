#!/usr/bin/env python3

#Advent of Code
#2018 Day 1, Part 1
#Solution by James C. (https://github.com/JamesMCo)

import os, sys
sys.path.append(os.path.abspath("../.."))
import unittest, util.read
from util.tests import run

def solve(puzzle_input):
    return sum(int(x) for x in puzzle_input)

def main():
    puzzle_input = util.read.as_lines()

    freq = solve(puzzle_input)

    print("The resulting frequency is " + str(freq) + ".")

class AOC_Tests(unittest.TestCase):
    def test_ex1(self):
        self.assertEqual(solve(["+1", "-2", "+3", "+1"]), 3)

    def test_ex2(self):
        self.assertEqual(solve(["+1", "+1", "-2"]), 0)

    def test_ex3(self):
        self.assertEqual(solve(["-1", "-2", "-3"]), -6)

run(main)
