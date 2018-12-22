#!/usr/bin/env python3

#Advent of Code
#2018 Day 21, Part 2
#Solution by James C. (https://github.com/JamesMCo)

import os, sys
sys.path.append(os.path.abspath("../.."))
import unittest, util.read
from util.tests import run

def solve(puzzle_input):
    potential = set()

    l6 = int(puzzle_input[7].split()[2])
    l7 = int(puzzle_input[8].split()[1])
    l8 = int(puzzle_input[9].split()[2])
    l10 = int(puzzle_input[11].split()[2])
    l11 = int(puzzle_input[12].split()[2])
    l12 = int(puzzle_input[13].split()[2])
    l13 = int(puzzle_input[14].split()[1])
    l19 = int(puzzle_input[20].split()[2])

    a, b, c, d = 0, 0, 0, 0
    skip_to_8 = False
    while True:
        if not skip_to_8:
            c = d | l6
            d = l7
        skip_to_8 = False
        b = c & l8
        d += b
        d &= l10
        d *= l11
        d &= l12
        if 256 > c:
            if d in potential:
                return last
            else:
                potential.add(d)
                last = d
        else:
            b = 0
            while True:
                a = b + 1
                a *= l19
                if a > c:
                    c = b
                    skip_to_8 = True
                    break
                else:
                    b += 1
                    continue

def main():
    puzzle_input = util.read.as_lines()

    value = solve(puzzle_input)

    print("The lowest non-negative integer value that causes the program to halt with the most instructions is " + str(value) + ".")

class AOC_Tests(unittest.TestCase):
    @unittest.skip("No test cases")
    def test_ex1(self):
        pass

run(main)
