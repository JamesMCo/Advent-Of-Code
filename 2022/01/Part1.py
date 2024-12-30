#!/usr/bin/env python3

#Advent of Code
#2022 Day 1, Part 1
#Solution by James C. (https://github.com/JamesMCo)

import os, sys
sys.path.append(os.path.abspath("../.."))
import unittest, util.read
from util.tests import run

def solve(puzzle_input):
    elves = [0]
    for line in puzzle_input:
        if line == "":
            elves.append(0)
        else:
            elves[-1] += int(line)

    return max(elves)

def main():
    puzzle_input = util.read.as_lines()

    calories = solve(puzzle_input)

    print("The elf with the highest number of calories is carrying " + str(calories) + " calories.")

class AOC_Tests(unittest.TestCase):
    def test_ex1(self):
        return self.assertEqual(solve(["1000",
                                       "2000",
                                       "3000",
                                       "",
                                       "4000",
                                       "",
                                       "5000",
                                       "6000",
                                       "",
                                       "7000",
                                       "8000",
                                       "9000",
                                       "",
                                       "10000"]), 24000)

if __name__ == "__main__":
    run(main)
