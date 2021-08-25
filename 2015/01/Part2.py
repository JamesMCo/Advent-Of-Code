#!/usr/bin/env python3

#Advent of Code
#2015 Day 1, Part 2
#Solution by James C. (https://github.com/JamesMCo)

import os, sys
sys.path.append(os.path.abspath("../.."))
import unittest, util.read
from util.tests import run

def solve(puzzle_input):
    floor = 0

    for i, x in enumerate(puzzle_input):
        if x == "(":
            floor += 1
        else:
            floor -= 1
        if floor < 0:
            return i + 1

def main():
    puzzle_input = util.read.as_string()

    pos = solve(puzzle_input)

    print("The position of the character that causes Santa to enter the basement is " + str(pos) + ".")

class AOC_Tests(unittest.TestCase):
    def test_ex1(self):
        return self.assertEqual(solve(")"), 1)

    def test_ex2(self):
        return self.assertEqual(solve("()())"), 5)

run(main)
