#!/usr/bin/env python3

#Advent of Code
#2022 Day 20, Part 2
#Solution by James C. (https://github.com/JamesMCo)

import os, sys
sys.path.append(os.path.abspath("../.."))
import unittest, util.read
from util.tests import run

from collections import deque

def solve(puzzle_input):
    class Number:
        def __init__(self, val):
            self.val = val

        def mix(self, l):
            l.rotate(-1-l.index(self))
            l.pop()
            l.rotate(-self.val)
            l.append(self)

        def move_to_start(self, l):
            l.rotate(-l.index(self))
    
    puzzle_input = [Number(n*811589153) for n in puzzle_input]
    file = deque(puzzle_input)
    for mix_round in range(10):
        for n in puzzle_input:
            n.mix(file)

    # Rotate such that 0 is at index 0
    for n in puzzle_input:
        if n.val == 0:
            n.move_to_start(file)

    ns = len(puzzle_input)
    return file[1000 % ns].val + file[2000 % ns].val + file[3000 % ns].val

def main():
    puzzle_input = util.read.as_int_list("\n")

    grove_coordinates = solve(puzzle_input)

    print("The sum of the three numbers that form the grove coordinates is " + str(grove_coordinates) + ".")

class AOC_Tests(unittest.TestCase):
    def test_ex1(self):
        return self.assertEqual(solve([1, 2, -3, 3, -2, 0, 4]), 1623178306)

run(main)
