#!/usr/bin/env python3

#Advent of Code
#2019 Day 19, Part 1
#Solution by James C. (https://github.com/JamesMCo)

import os, sys
sys.path.append(os.path.abspath("../.."))
import unittest, util.read
from util.tests import run

from util.intcode_2019 import IntcodeComputer

def solve(puzzle_input):
    computer = IntcodeComputer().load_memory(puzzle_input)

    def query(coords):
        computer.reset().queue_inputs(coords)
        while not computer.outputs:
            computer.step()
        return computer.outputs[0]

    return sum(query((x, y)) for x in range(50) for y in range(50))

def main():
    puzzle_input = util.read.as_int_list(",")

    points = solve(puzzle_input)

    print("The number of points affected by the tractor beam in the 50x50 area closest to the emitter is " + str(points) + ".")

class AOC_Tests(unittest.TestCase):
    @unittest.skip("No test cases")
    def test_ex1(self):
        pass

run(main)
