#!/usr/bin/env python3

#Advent of Code
#2017 Day 17, Part 1
#Solution by James C. (https://github.com/JamesMCo)

import os, sys
sys.path.append(os.path.abspath("../.."))
import unittest, util.read
from util.tests import run

def solve(puzzle_input):        
    buffer = [0]
    current = 0

    for i in range(1, 2018):
        current = (current + puzzle_input) % len(buffer) + 1
        buffer.insert(current, i)

    return buffer[(buffer.index(2017) + 1) % len(buffer)]

def main():
    puzzle_input = util.read.as_int()

    value = solve(puzzle_input)

    print("The value after the last value written is " + str(value) + ".")

class AOC_Tests(unittest.TestCase):
    def test_ex1(self):
        self.assertEqual(solve(3), 638)

if __name__ == "__main__":
    run(main)
