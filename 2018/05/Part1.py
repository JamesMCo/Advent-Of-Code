#!/usr/bin/env python3

#Advent of Code
#Day 5, Part 1
#Solution by James C. (https://github.com/JamesMCo)

import os, sys, colorama, time
sys.path.append(os.path.abspath("../.."))
import unittest
from util.tests import run

import string

def solve(puzzle_input):
    def react(polymer):
        units = []
        for u in polymer:
            if len(units) > 0:
                if units[-1].swapcase() == u:
                    units.pop()
                else:
                    units.append(u)
            else:
                units.append(u)
        return "".join(units)

    return len(react(puzzle_input))

def main():
    f = open("puzzle_input.txt")
    puzzle_input = f.read().strip()
    f.close()

    units = solve(puzzle_input)

    print("The number of remaining units is " + str(units) + ".")

class AOC_Tests(unittest.TestCase):
    def test_ex1(self):
        self.assertEqual(solve("aA"), 0)

    def test_ex2(self):
        self.assertEqual(solve("abBA"), 0)

    def test_ex3(self):
        self.assertEqual(solve("abAB"), 4)

    def test_ex4(self):
        self.assertEqual(solve("aabAAB"), 6)

    def test_ex5(self):
        self.assertEqual(solve("dabAcCaCBAcCcaDA"), 10)

run(main)
