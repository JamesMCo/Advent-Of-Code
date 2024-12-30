#!/usr/bin/env python3

#Advent of Code
#2017 Day 6, Part 2
#Solution by James C. (https://github.com/JamesMCo)

import os, sys
sys.path.append(os.path.abspath("../.."))
import unittest, util.read
from util.tests import run

def solve(puzzle_input):
    history = []
    length = len(puzzle_input)

    while str(puzzle_input) not in history:
        history.append(str(puzzle_input))
        i = j = puzzle_input.index(max(puzzle_input))
        c = puzzle_input[i]
        puzzle_input[j] = 0
        j = (i + 1) % length
        while c > 0:
            puzzle_input[j] += 1
            c -= 1
            j = (j + 1) % length

    return len(history) - history.index(str(puzzle_input))

def main():
    puzzle_input = [int(x) for x in util.read.as_string().split() if x != ""]

    cycles = solve(puzzle_input)

    print("The number of redistribution cycles in the infinite loop is " + str(cycles) + ".")

class AOC_Tests(unittest.TestCase):
    def test_ex1(self):
        self.assertEqual(solve([0, 2, 7, 0]), 4)

if __name__ == "__main__":
    run(main)
