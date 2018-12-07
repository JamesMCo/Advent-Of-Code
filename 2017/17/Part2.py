#!/usr/bin/env python3

#Advent of Code
#Day 17, Part 2
#Solution by James C. (https://github.com/JamesMCo)

import os, sys
sys.path.append(os.path.abspath("../.."))
import unittest, util.read
from util.tests import run

def solve(puzzle_input):        
    current = 0
    length = 1
    result = 0

    for i in range(1, 50000000):
        current = (current + puzzle_input) % length + 1
        if current == 1:
            result = i
        length += 1

    return result

def main():
    puzzle_input = util.read.as_int()

    value = solve(puzzle_input)

    print("The value after the 0 is " + str(value) + ".")

class AOC_Tests(unittest.TestCase):
    def test_ex1(self):
        self.assertEqual(solve(3), 1222153)

run(main)
