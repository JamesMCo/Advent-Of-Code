#!/usr/bin/env python3

#Advent of Code
#Day 9, Part 2
#Solution by James C. (https://github.com/JamesMCo)

import os, sys
sys.path.append(os.path.abspath("../.."))
import unittest
from util.tests import run

def solve(puzzle_input):
    count = 0

    i = 0
    while i < len(puzzle_input):
        if puzzle_input[i] == "!":
            puzzle_input = puzzle_input[:i] + puzzle_input[i+2:]
        else:
            i += 1        

    i = 0
    in_garbage = False
    while i < len(puzzle_input):
        if in_garbage:
            if puzzle_input[i] == ">":
                in_garbage = False
            else:
                count += 1
        elif puzzle_input[i] == "<":
            in_garbage = True
        i += 1

    return count

def main():
    f = open("puzzle_input.txt")
    puzzle_input = f.read()[:-1]
    f.close()

    count = solve(puzzle_input)

    print("The number of non-cancelled charcters whithin the garbage is " + str(count) + ".")

class AOC_Tests(unittest.TestCase):
    def test_ex1(self):
        self.assertEqual(solve("<>"), 0)

    def test_ex2(self):
        self.assertEqual(solve("<random characters>"), 17)

    def test_ex3(self):
        self.assertEqual(solve("<<<<>"), 3)

    def test_ex4(self):
        self.assertEqual(solve("<{!>}>"), 2)

    def test_ex5(self):
        self.assertEqual(solve("<!!>"), 0)

    def test_ex6(self):
        self.assertEqual(solve("<!!!>>"), 0)

    def test_ex7(self):
        self.assertEqual(solve("<{o\"i!a,<{i<a>"), 10)

run(main)
