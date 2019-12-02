#!/usr/bin/env python3

#Advent of Code
#2019 Day 2, Part 1
#Solution by James C. (https://github.com/JamesMCo)

import os, sys
sys.path.append(os.path.abspath("../.."))
import unittest, util.read
from util.tests import run

def solve(puzzle_input):
    i = 0
    while True:
        opcode = puzzle_input[i]
        if opcode == 1:
            puzzle_input[puzzle_input[i+3]] = puzzle_input[puzzle_input[i+1]] + puzzle_input[puzzle_input[i+2]]
            i += 4
        elif opcode == 2:
            puzzle_input[puzzle_input[i+3]] = puzzle_input[puzzle_input[i+1]] * puzzle_input[puzzle_input[i+2]]
            i += 4
        elif opcode == 99:
            return puzzle_input

def main():
    puzzle_input = util.read.as_int_list(",")
    puzzle_input[1] = 12
    puzzle_input[2] = 2

    state = solve(puzzle_input)

    print("The value at position 0 after the program halts is " + str(state[0]) + ".")

class AOC_Tests(unittest.TestCase):
    def test_ex1(self):
        self.assertEqual(solve([1,    9, 10,  3, 2, 3, 11, 0, 99, 30, 40, 50]),
                               [3500, 9, 10, 70, 2, 3, 11, 0, 99, 30, 40, 50])

    def test_ex2(self):
        self.assertEqual(solve([1, 0, 0, 0, 99]),
                               [2, 0, 0, 0, 99])

    def test_ex3(self):
        self.assertEqual(solve([2, 3, 0, 3, 99]),
                               [2, 3, 0, 6, 99])

    def test_ex4(self):
        self.assertEqual(solve([2, 4, 4, 5, 99, 0]),
                               [2, 4, 4, 5, 99, 9801])

    def test_ex5(self):
        self.assertEqual(solve([1, 1, 1,  4, 99, 5, 6, 0, 99]),
                               [30, 1, 1, 4,  2, 5, 6, 0, 99])

run(main)
