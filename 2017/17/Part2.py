#!/usr/bin/env python3

#Advent of Code
#Day 17, Part 2
#Solution by James C. (https://github.com/JamesMCo)

import os, sys
sys.path.append(os.path.abspath("../.."))
import unittest
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
    f = open("puzzle_input.txt")
    puzzle_input = int(f.read()[:-1])
    f.close()

    value = solve(puzzle_input)

    print("The value after the 0 is " + str(value) + ".")

class AOC_Tests(unittest.TestCase):
    def test_ex1(self):
        self.assertEqual(solve(3), 1222153)

run(main)
