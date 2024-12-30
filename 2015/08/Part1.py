#!/usr/bin/env python3

#Advent of Code
#2015 Day 8, Part 1
#Solution by James C. (https://github.com/JamesMCo)

import os, sys
sys.path.append(os.path.abspath("../.."))
import unittest, util.read
from util.tests import run

def solve(puzzle_input):
    literals = 0
    memory = 0

    for i in puzzle_input:
        literals += len(i)
        memory += len(eval(i))

    return literals - memory

def main():
    puzzle_input = util.read.as_lines()

    v = solve(puzzle_input)

    print("The number of characters of code for literals minus the values of the strings is " + str(v) + ".")

class AOC_Tests(unittest.TestCase):
    def test_ex1(self):
        return self.assertEqual(solve(["\"\"",
                                       "\"abc\"",
                                       "\"aaa\\\"aaa\"",
                                       "\"\\x27\""]), 12)

if __name__ == "__main__":
    run(main)
