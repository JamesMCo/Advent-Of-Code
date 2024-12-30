#!/usr/bin/env python3

#Advent of Code
#2015 Day 2, Part 2
#Solution by James C. (https://github.com/JamesMCo)

import os, sys
sys.path.append(os.path.abspath("../.."))
import unittest, util.read
from util.tests import run

def solve(puzzle_input):
    total = 0

    for i in puzzle_input:
        current = i.split("x")
        side1 = 2 * int(current[0]) + 2 * int(current[1])
        side2 = 2 * int(current[1]) + 2 * int(current[2])
        side3 = 2 * int(current[2]) + 2 * int(current[0])

        perimeters = [side1, side2, side3]
        perimeters.sort()
        total += perimeters[0]
        total += int(current[0]) * int(current[1]) * int(current[2])

    return total

def main():
    puzzle_input = util.read.as_lines()

    total = solve(puzzle_input)

    print("The number of feet of ribbon the elves should order is " + str(total) + ".")

class AOC_Tests(unittest.TestCase):
    def test_ex1(self):
        return self.assertEqual(solve(["2x3x4"]), 34)

    def test_ex2(self):
        return self.assertEqual(solve(["1x1x10"]), 14)

if __name__ == "__main__":
    run(main)
