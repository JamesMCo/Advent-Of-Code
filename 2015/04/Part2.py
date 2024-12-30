#!/usr/bin/env python3

#Advent of Code
#2015 Day 4, Part 2
#Solution by James C. (https://github.com/JamesMCo)

import os, sys
sys.path.append(os.path.abspath("../.."))
import unittest, util.read
from util.tests import run

import hashlib

def solve(puzzle_input):
    i = 0
    while True:
        current_hash = hashlib.md5(str(puzzle_input + str(i)).encode("utf-8")).hexdigest()
        if current_hash[0:6] == "000000":
            return i
        i += 1

def main():
    puzzle_input = util.read.as_string()

    i = solve(puzzle_input)

    print("The lowest positive integer to produce a hash is " + str(i) + ".")

class AOC_Tests(unittest.TestCase):
    @unittest.skip("No test cases")
    def test_ex1(self):
        pass

if __name__ == "__main__":
    run(main)
