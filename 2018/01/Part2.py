#!/usr/bin/env python3

#Advent of Code
#Day 1, Part 2
#Solution by James C. (https://github.com/JamesMCo)

import os, sys
sys.path.append(os.path.abspath("../.."))
import unittest, util.read
from util.tests import run

def solve(puzzle_input):
    freq = 0
    seen = set([0])

    while True:
        for f in puzzle_input:
            if f[0] == "+":
                freq += int(f[1:])
            else:
                freq -= int(f[1:])

            if freq in seen:
                return freq
            else:
                seen.add(freq)

def main():
    puzzle_input = util.read.as_lines()

    freq = solve(puzzle_input)

    print("The resulting frequency is " + str(freq) + ".")

class AOC_Tests(unittest.TestCase):
    def test_ex1(self):
        self.assertEqual(solve(["+1", "-2", "+3", "+1"]), 2)

    def test_ex2(self):
        self.assertEqual(solve(["+1", "-1"]), 0)

    def test_ex3(self):
        self.assertEqual(solve(["+3", "+3", "+4", "-2", "-4"]), 10)

    def test_ex4(self):
        self.assertEqual(solve(["-6", "+3", "+8", "+5", "-6"]), 5)

    def test_ex5(self):
        self.assertEqual(solve(["+7", "+7", "-2", "-7", "-4"]), 14)

run(main)
