#!/usr/bin/env python3

#Advent of Code
#2021 Day 3, Part 1
#Solution by James C. (https://github.com/JamesMCo)

import os, sys
sys.path.append(os.path.abspath("../.."))
import unittest, util.read
from util.tests import run

from collections import Counter

def solve(puzzle_input):
    counts = [Counter() for i in range(len(puzzle_input[0]))]
    for number in puzzle_input:
        for i, d in enumerate(number):
            counts[i].update(d)

    epsilon = int("".join(c.most_common()[0][0] for c in counts), 2)
    gamma   = int("".join(c.most_common()[1][0] for c in counts), 2)
    return epsilon * gamma

def main():
    puzzle_input = util.read.as_lines()

    power = solve(puzzle_input)

    print("The power consumption is " + str(power) + ".")

class AOC_Tests(unittest.TestCase):
    def test_ex1(self):
        return self.assertEqual(solve(["00100",
                                       "11110",
                                       "10110",
                                       "10111",
                                       "10101",
                                       "01111",
                                       "00111",
                                       "11100",
                                       "10000",
                                       "11001",
                                       "00010",
                                       "01010"]), 198)

run(main)
