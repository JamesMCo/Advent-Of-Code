#!/usr/bin/env python3

#Advent of Code
#2020 Day 25, Part 1
#Solution by James C. (https://github.com/JamesMCo)

import os, sys
sys.path.append(os.path.abspath("../.."))
import unittest, util.read
from util.tests import run

def solve(puzzle_input):
    def transform(subject_number, loop_size):
        # Originally calculated manually, but changed to use
        # the function pow after it took unreasonably long
        # to arrive at an answern and I checked others' solutions
        # on the subreddit
        return pow(subject_number, loop_size, 20201227)

    loop_size = 0
    while True:
        candidate = transform(7, loop_size)
        if candidate == puzzle_input[0]:
            return transform(puzzle_input[1], loop_size)
        elif candidate == puzzle_input[1]:
            return transform(puzzle_input[0], loop_size)
        loop_size += 1

def main():
    puzzle_input = util.read.as_int_list("\n")

    encryption_key = solve(puzzle_input)

    print("The encryption key is " + str(encryption_key) + ".")

class AOC_Tests(unittest.TestCase):
    def test_ex1(self):
        return self.assertEqual(solve([5764801, 17807724]), 14897079)

if __name__ == "__main__":
    run(main)
