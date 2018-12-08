#!/usr/bin/env python3

#Advent of Code
#Day 1, Part 1
#Solution by James C. (https://github.com/JamesMCo)

import os, sys
sys.path.append(os.path.abspath("../.."))
import unittest, util.read
from util.tests import run

def solve(puzzle_input):
    freq = 0

    for f in puzzle_input:
        if f[0] == "+":
            freq += int(f[1:])
        else:
            freq -= int(f[1:])

    return freq

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
