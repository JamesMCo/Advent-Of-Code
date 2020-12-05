#!/usr/bin/env python3

#Advent of Code
#2020 Day 5, Part 2
#Solution by James C. (https://github.com/JamesMCo)

import os, sys
sys.path.append(os.path.abspath("../.."))
import unittest, util.read
from util.tests import run

def solve(puzzle_input):
    seats = sorted(int(boarding_pass.replace("F", "0").replace("B", "1").replace("L", "0").replace("R", "1"), 2) for boarding_pass in puzzle_input)
    for expected, actual in zip(range(seats[0], seats[-1]+1), seats):
        if expected != actual:
            return expected

def main():
    puzzle_input = util.read.as_lines()

    seat_id = solve(puzzle_input)

    print("The seat ID is " + str(seat_id) + ".")

class AOC_Tests(unittest.TestCase):
    @unittest.skip("No test cases")
    def test_ex1(self):
        pass

run(main)
