#!/usr/bin/env python3

#Advent of Code
#2017 Day 1, Part 2
#Solution by James C. (https://github.com/JamesMCo)

import os, sys
sys.path.append(os.path.abspath("../.."))
import unittest, util.read
from util.tests import run

def solve(puzzle_input):
    total = 0
    half = int(len(puzzle_input) / 2)

    for i, x in enumerate(puzzle_input):
        if puzzle_input[i] == puzzle_input[(i+half) % len(puzzle_input)]:
            total += int(x)

    return total

def main():
    puzzle_input = util.read.as_string()

    total = solve(puzzle_input)

    print("The solution to the captcha is " + str(total) + ".")

class AOC_Tests(unittest.TestCase):
    def test_ex1(self):
        self.assertEqual(solve("1212"), 6)

    def test_ex2(self):
        self.assertEqual(solve("1221"), 0)

    def test_ex3(self):
        self.assertEqual(solve("123425"), 4)

    def test_ex4(self):
        self.assertEqual(solve("123123"), 12)

    def test_ex5(self):
        self.assertEqual(solve("12131415"), 4)

if __name__ == "__main__":
    run(main)
