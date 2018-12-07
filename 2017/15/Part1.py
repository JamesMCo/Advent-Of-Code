#!/usr/bin/env python3

#Advent of Code
#Day 15, Part 1
#Solution by James C. (https://github.com/JamesMCo)

import os, sys
sys.path.append(os.path.abspath("../.."))
import unittest, util.read
from util.tests import run

def solve(puzzle_input):
    gena = puzzle_input[0]
    genb = puzzle_input[1]
    count = 0

    for i in range(40000000):
        gena = (gena * 16807) % 2147483647
        genb = (genb * 48271) % 2147483647

        if bin(gena)[2:].zfill(32)[16:] == bin(genb)[2:].zfill(32)[16:]:
            count += 1
    
    return count

def main():
    puzzle_input = [int(x.split(" ")[-1]) for x in util.read.as_lines()]

    count = solve(puzzle_input)

    print("The judge's final count is " + str(count) + ".")

class AOC_Tests(unittest.TestCase):
    def test_ex1(self):
        self.assertEqual(solve([65, 8921]), 588)

run(main)
