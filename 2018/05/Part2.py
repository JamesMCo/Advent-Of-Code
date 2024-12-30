#!/usr/bin/env python3

#Advent of Code
#2018 Day 5, Part 2
#Solution by James C. (https://github.com/JamesMCo)

import os, sys
sys.path.append(os.path.abspath("../.."))
import unittest, util.read
from util.tests import run

import string

def solve(puzzle_input):
    def react(polymer):
        units = []
        for u in polymer:
            if len(units) > 0:
                if units[-1].swapcase() == u:
                    units.pop()
                else:
                    units.append(u)
            else:
                units.append(u)
        return "".join(units)

    lengths = []
    for u in string.ascii_lowercase:
        if u in puzzle_input.lower():
            lengths.append(len(react(puzzle_input.replace(u, "").replace(u.upper(), ""))))
    
    return min(lengths)

def main():
    puzzle_input = util.read.as_string()

    units = solve(puzzle_input)

    print("The length of the shortest polymer you can produce is " + str(units) + ".")

class AOC_Tests(unittest.TestCase):
    def test_ex1(self):
        self.assertEqual(solve("dabAcCaCBAcCcaDA"), 4)

if __name__ == "__main__":
    run(main)
