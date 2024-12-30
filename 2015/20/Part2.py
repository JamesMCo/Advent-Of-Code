#!/usr/bin/env python3

#Advent of Code
#2015 Day 20, Part 2
#Solution by James C. (https://github.com/JamesMCo)

import os, sys
sys.path.append(os.path.abspath("../.."))
import unittest, util.read
from util.tests import run

def solve(puzzle_input):
    def factors(n):
        pairs = [(f, int(n/f)) for f in range(1, int(n**0.5 + 1)) if n % f == 0]
        unique = set()
        for pair in pairs:
            if n <= pair[0] * 50:
                unique.add(pair[0])
            if n <= pair[1] * 50:
                unique.add(pair[1])
        return list(unique)

    i = 1
    while sum(factors(i)) * 11 < puzzle_input:
        i += 1
    return i

def main():
    puzzle_input = util.read.as_int()

    house = solve(puzzle_input)

    print("The lowest house number that gets at least as many presents as the puzzle input is " + str(house) + ".")

class AOC_Tests(unittest.TestCase):
    @unittest.skip("No test cases")
    def test_ex1(self):
        pass

if __name__ == "__main__":
    run(main)
