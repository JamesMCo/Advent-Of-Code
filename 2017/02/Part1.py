#!/usr/bin/env python3

#Advent of Code
#Day 2, Part 1
#Solution by James C. (https://github.com/JamesMCo)

import os, sys
sys.path.append(os.path.abspath("../.."))
import unittest, util.tests

def solve(puzzle_input):
    checksum = 0

    for row in puzzle_input:
        temp = [int(x) for x in row.split(" ") if x != ""]
        checksum += max(temp) - min(temp)

    return checksum

def main():
    f = open("puzzle_input.txt")
    puzzle_input = f.read()[:-1].split("\n")
    f.close()

    checksum = solve(puzzle_input)

    print("The checksum of the spreadsheet is " + str(checksum) + ".")

class AOC_Tests(unittest.TestCase):
    def test_ex1(self):
        self.assertEqual(solve(["5 1 9 5", "7 5 3", "2 4 6 8"]), 18)

if __name__ == "__main__":
    if unittest.main(verbosity=2, exit=False, testRunner=util.tests.Runner).result.wasSuccessful():
        main()
        exit(0)
    else:
        exit(1)
