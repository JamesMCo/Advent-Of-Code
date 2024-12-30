#!/usr/bin/env python3

#Advent of Code
#2020 Day 9, Part 2
#Solution by James C. (https://github.com/JamesMCo)

import os, sys
sys.path.append(os.path.abspath("../.."))
import unittest, util.read
from util.tests import run

from collections import deque
from itertools import combinations

def solve(puzzle_input, preamble_size=25):
    working = deque(puzzle_input[:preamble_size])

    for n in puzzle_input[preamble_size:]:
        if not any(a + b == n for a, b in combinations(working, 2)):
            target = n
            break

        working.popleft()
        working.append(n)

    for i in range(len(puzzle_input)):
        working = 0
        j = i
        while working < target:
            working += puzzle_input[j]
            j += 1
        if working == target and j != i:
            return min(puzzle_input[i:j]) + max(puzzle_input[i:j])

def main():
    puzzle_input = util.read.as_int_list("\n")

    weakness = solve(puzzle_input)

    print("The encryption weakness in the XMAS-encrypted list of numbers is " + str(weakness) + ".")

class AOC_Tests(unittest.TestCase):
    def test_ex1(self):
        return self.assertEqual(solve([ 35,  20,  15,  25,  47,
                                        40,  62,  55,  65,  95,
                                       102, 117, 150, 182, 127,
                                       219, 299, 277, 309, 576], 5), 62)

if __name__ == "__main__":
    run(main)
