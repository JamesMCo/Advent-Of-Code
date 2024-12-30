#!/usr/bin/env python3

#Advent of Code
#2022 Day 4, Part 2
#Solution by James C. (https://github.com/JamesMCo)

import os, sys
sys.path.append(os.path.abspath("../.."))
import unittest, util.read
from util.tests import run

import re

def solve(puzzle_input):
    def parse_assignments(pair):
        first_lower, first_upper, second_lower, second_upper = [int(x) for x in re.match(r"(\d+)-(\d+),(\d+)-(\d+)", pair).groups()]
        return (first_lower, first_upper), (second_lower, second_upper)

    def overlap(first, second):
        return first[0]  <= second[0] <= first[1]  or \
               first[0]  <= second[1] <= first[1]  or \
               second[0] <= first[0]  <= second[1] or \
               second[0] <= first[1]  <= second[1]

    return len([(first, second) for first, second in [parse_assignments(pair) for pair in puzzle_input] if overlap(first, second)])

def main():
    puzzle_input = util.read.as_lines()

    pairs = solve(puzzle_input)

    print("The number of pairs where the assignments overlap is " + str(pairs) + ".")

class AOC_Tests(unittest.TestCase):
    def test_ex1(self):
        return self.assertEqual(solve(["2-4,6-8",
                                       "2-3,4-5",
                                       "5-7,7-9",
                                       "2-8,3-7",
                                       "6-6,4-6",
                                       "2-6,4-8"]), 4)

if __name__ == "__main__":
    run(main)
