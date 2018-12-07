#!/usr/bin/env python3

#Advent of Code
#Day 2, Part 1
#Solution by James C. (https://github.com/JamesMCo)

import os, sys, colorama, time
sys.path.append(os.path.abspath("../.."))
import unittest, util.read
from util.tests import run

import string

def solve(puzzle_input):
    twos = 0
    threes = 0

    for i in puzzle_input:
        if sum([1 for x in string.ascii_lowercase if i.count(x) == 2]) >= 1:
            twos += 1

        if sum([1 for x in string.ascii_lowercase if i.count(x) == 3]) >= 1:
            threes += 1
    
    return twos * threes

def main():
    puzzle_input = util.read.as_lines()

    checksum = solve(puzzle_input)

    print("The checksum is " + str(checksum) + ".")

class AOC_Tests(unittest.TestCase):
    def test_ex1(self):
        self.assertEqual(solve(["abcdef"
                                "bababc",
                                "abbcde",
                                "abcccd",
                                "aabcdd",
                                "abcdee",
                                "ababab"]), 12)

run(main)
