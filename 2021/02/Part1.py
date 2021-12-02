#!/usr/bin/env python3

#Advent of Code
#2021 Day 2, Part 1
#Solution by James C. (https://github.com/JamesMCo)

import os, sys
sys.path.append(os.path.abspath("../.."))
import unittest, util.read
from util.tests import run

def solve(puzzle_input):
    horizontal = 0
    depth = 0

    for command in puzzle_input:
        match command.split():
            case ("forward", n):
                horizontal += int(n)
            case ("down", n):
                depth += int(n)
            case ("up", n):
                depth -= int(n)
    
    return horizontal * depth

def main():
    puzzle_input = util.read.as_lines()

    product = solve(puzzle_input)

    print("The product of the final horizontal position and depth is " + str(product) + ".")

class AOC_Tests(unittest.TestCase):
    def test_ex1(self):
        return self.assertEqual(solve(["forward 5",
                                       "down 5",
                                       "forward 8",
                                       "up 3",
                                       "down 8",
                                       "forward 2"]), 150)

run(main)
