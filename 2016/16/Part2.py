#!/usr/bin/env python3

#Advent of Code
#2016 Day 16, Part 2
#Solution by James C. (https://github.com/JamesMCo)

import os, sys
sys.path.append(os.path.abspath("../.."))
import unittest, util.read
from util.tests import run

def solve(puzzle_input, required_length=35651584):
    state = puzzle_input

    def step(a):
        return a + "0" + a[::-1].replace("1", "-").replace("0", "1").replace("-", "0")

    def checksum(a):
        o = ""
        for i in range(0, len(a)-1, 2):
            if a[i] == a[i+1]:
                o += "1"
            else:
                o += "0"
        if len(o) % 2 == 0:
            return checksum(o)
        return o

    while len(state) < required_length:
        state = step(state)

    return checksum(state[:required_length])

def main():
    puzzle_input = util.read.as_string()

    checksum = solve(puzzle_input)

    print("The correct checksum is " + str(checksum) + ".")

class AOC_Tests(unittest.TestCase):
    @unittest.skip("No test cases")
    def test_ex1(self):
        pass

if __name__ == "__main__":
    run(main)
