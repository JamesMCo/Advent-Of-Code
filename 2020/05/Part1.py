#!/usr/bin/env python3

#Advent of Code
#2020 Day 5, Part 1
#Solution by James C. (https://github.com/JamesMCo)

import os, sys
sys.path.append(os.path.abspath("../.."))
import unittest, util.read
from util.tests import run

def solve(puzzle_input):
    return max(int(boarding_pass.replace("F", "0").replace("B", "1").replace("L", "0").replace("R", "1"), 2) for boarding_pass in puzzle_input)

def main():
    puzzle_input = util.read.as_lines()

    highest_seat_id = solve(puzzle_input)

    print("The highest seat ID is " + str(highest_seat_id) + ".")

class AOC_Tests(unittest.TestCase):
    def test_ex1(self):
        return self.assertEqual(solve(["FBFBBFFRLR"]), 357)

    def test_ex2(self):
        return self.assertEqual(solve(["BFFFBBFRRR"]), 567)

    def test_ex3(self):
        return self.assertEqual(solve(["FFFBBBFRRR"]), 119)

    def test_ex4(self):
        return self.assertEqual(solve(["BBFFBBFRLL"]), 820)

if __name__ == "__main__":
    run(main)
