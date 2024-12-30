#!/usr/bin/env python3

#Advent of Code
#2019 Day 17, Part 1
#Solution by James C. (https://github.com/JamesMCo)

import os, sys
sys.path.append(os.path.abspath("../.."))
import unittest, util.read
from util.tests import run

from util.two_d_world import World
from util.intcode_2019 import IntcodeComputer

def solve(puzzle_input):
    computer = IntcodeComputer().load_memory(puzzle_input).run()
    grid = World(".", True)
    grid.load_from_lists("".join(map(chr, computer.outputs)).split("\n"))

    def neighbours(x, y):
        yield from [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)]

    def is_scaffolding(cell):
        return grid[cell] != "."

    def alignment_parameter(cell):
        if is_scaffolding(cell) and all(map(is_scaffolding, neighbours(*cell))):
            return cell[0] * cell[1]
        else:
            return 0

    return sum(map(alignment_parameter, list(grid.keys())))

def main():
    puzzle_input = util.read.as_int_list(",")

    alignment_params = solve(puzzle_input)

    print("The sum of the alignment parameters is " + str(alignment_params) + ".")

class AOC_Tests(unittest.TestCase):
    @unittest.skip("No test cases")
    def test_ex1(self):
        pass

if __name__ == "__main__":
    run(main)
