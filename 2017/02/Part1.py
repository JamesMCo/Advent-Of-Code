#!/usr/bin/env python3

#Advent of Code
#Day 2, Part 1
#Solution by James C. (https://github.com/JamesMCo)

import os, sys
sys.path.append(os.path.abspath("../.."))
import unittest, util.read
from util.tests import run

def solve(puzzle_input):
    checksum = 0

    for row in puzzle_input:
        temp = [int(x) for x in row.split(" ") if x != ""]
        checksum += max(temp) - min(temp)

    return checksum

def main():
    puzzle_input = util.read.as_lines()

    checksum = solve(puzzle_input)

    print("The checksum of the spreadsheet is " + str(checksum) + ".")

class AOC_Tests(unittest.TestCase):
    def test_ex1(self):
        self.assertEqual(solve(["5 1 9 5", "7 5 3", "2 4 6 8"]), 18)

run(main)
