#!/usr/bin/env python3

#Advent of Code
#Day 5, Part 2
#Solution by James C. (https://github.com/JamesMCo)

import os, sys
sys.path.append(os.path.abspath("../.."))
import unittest
from util.tests import run

def solve(puzzle_input):
    i = 0
    steps = 0
    length = len(puzzle_input)

    while 0 <= i < length:
        t = puzzle_input[i]
        if puzzle_input[i] >= 3:
            puzzle_input[i] -= 1
        else:
            puzzle_input[i] += 1
        i += t
        steps += 1

    return steps

def main():
    f = open("puzzle_input.txt")
    puzzle_input = [int(x) for x in f.read()[:-1].split("\n")]
    f.close()

    steps = solve(puzzle_input)

    print("It takes " + str(steps) + " steps to reach the exit.")

class AOC_Tests(unittest.TestCase):
    def test_ex1(self):
        self.assertEqual(solve([0, 3, 0, 1, -3]), 10)

run(main)
