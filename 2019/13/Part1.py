#!/usr/bin/env python3

#Advent of Code
#2019 Day 13, Part 1
#Solution by James C. (https://github.com/JamesMCo)

import os, sys
sys.path.append(os.path.abspath("../.."))
import unittest, util.read
from util.tests import run

from itertools import islice
from util.intcode_2019 import IntcodeComputer

def solve(puzzle_input):
    i = IntcodeComputer().load_memory(puzzle_input).run()

    block_tiles = 0
    for tile in islice(i.outputs, 2, None, 3):
        if tile == 2:
            block_tiles += 1
    return block_tiles

def main():
    puzzle_input = util.read.as_int_list(",")

    block_tiles = solve(puzzle_input)

    print("The number of block tiles on screen when the game exits is " + str(block_tiles) + ".")

class AOC_Tests(unittest.TestCase):
    @unittest.skip("No test cases")
    def test_ex1(self):
        pass

run(main)
