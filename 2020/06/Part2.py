#!/usr/bin/env python3

#Advent of Code
#2020 Day 6, Part 2
#Solution by James C. (https://github.com/JamesMCo)

import os, sys
sys.path.append(os.path.abspath("../.."))
import unittest, util.read
from util.tests import run

def solve(puzzle_input):
    def consume_group():
        output = []
        while puzzle_input:
            line = puzzle_input.pop(0)
            if line == "":
                break
            output.append(set(line))
        return output[0].intersection(*output[1:])

    groups = []
    while puzzle_input:
        groups.append(consume_group())

    return sum(len(g) for g in groups)

def main():
    puzzle_input = util.read.as_lines()

    counts = solve(puzzle_input)

    print("The sum of the number of questions to which anyone answered \"yes\" for all groups is " + str(counts) + ".")

class AOC_Tests(unittest.TestCase):
    def test_ex1(self):
        return self.assertEqual(solve(["abc",
                                       "",
                                       "a",
                                       "b",
                                       "c",
                                       "",
                                       "ab",
                                       "ac",
                                       "",
                                       "a",
                                       "a",
                                       "a",
                                       "a",
                                       "",
                                       "b"]), 6)

run(main)
