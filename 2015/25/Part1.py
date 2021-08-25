#!/usr/bin/env python3

#Advent of Code
#2015 Day 25, Part 1
#Solution by James C. (https://github.com/JamesMCo)

import os, sys
sys.path.append(os.path.abspath("../.."))
import unittest, util.read
from util.tests import run

def solve(puzzle_input):
    row = int(puzzle_input[puzzle_input.index("row")+1][:-1])
    col = int(puzzle_input[puzzle_input.index("column")+1][:-1])
    codeno = 1 + sum(range(1, row)) + sum(range(row + 1, row + col))

    code = 20151125
    for i in range(codeno - 1):
        code = (code * 252533) % 33554393

    return code

def main():
    puzzle_input = util.read.as_string_list(" ")

    code = solve(puzzle_input)

    print("The code from the manual is " + str(code) + ".")

class AOC_Tests(unittest.TestCase):
    @unittest.skip("No test cases")
    def test_ex1(self):
        pass

run(main)
