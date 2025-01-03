#!/usr/bin/env python3

#Advent of Code
#2017 Day 2, Part 2
#Solution by James C. (https://github.com/JamesMCo)

import os, sys
sys.path.append(os.path.abspath("../.."))
import unittest, util.read
from util.tests import run

def solve(puzzle_input):
    checksum = 0

    for row in puzzle_input:
        temp = sorted([int(x) for x in row.split() if x != ""], reverse=True)
        found = False
        for i in range(len(temp)):
            for j in range(i + 1, len(temp)):
                if temp[i] % temp[j] == 0:
                    checksum += int(temp[i] / temp[j])
                    found = True
                    break
            if found:
                break

    return checksum    

def main():
    puzzle_input = util.read.as_lines()

    checksum = solve(puzzle_input)

    print("The checksum of the spreadsheet is " + str(checksum) + ".")

class AOC_Tests(unittest.TestCase):
    def test_ex1(self):
        self.assertEqual(solve(["5 9 2 8", "9 4 7 3", "3 8 6 5"]), 9)

if __name__ == "__main__":
    run(main)
