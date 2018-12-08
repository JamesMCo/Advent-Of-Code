#!/usr/bin/env python3

#Advent of Code
#2017 Day 23, Part 2
#Solution by James C. (https://github.com/JamesMCo)

import os, sys
sys.path.append(os.path.abspath("../.."))
import unittest, util.read
from util.tests import run

def solve(puzzle_input):
    h = 0

    start = (int(puzzle_input[0].split()[2]) * 100) + 100000
    end = start + 17000
    step = -int(puzzle_input[-2].split()[2])

    for i in range(start, end + 1, step):
        prime = True
        for j in range(2, int(i**0.5)):
            if i % j == 0:
                prime = False
                break
        h += not prime
    
    return h

def main():
    puzzle_input = util.read.as_lines()

    h = solve(puzzle_input)

    print("The value of register h is " + str(h) + ".")

class AOC_Tests(unittest.TestCase):
    def test_ex1(self):
        pass

run(main)
