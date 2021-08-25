#!/usr/bin/env python3

#Advent of Code
#2015 Day 5, Part 2
#Solution by James C. (https://github.com/JamesMCo)

import os, sys
sys.path.append(os.path.abspath("../.."))
import unittest, util.read
from util.tests import run

def solve(puzzle_input):
    nice = 0

    for i in puzzle_input:
        pairs = False
        gap = False

        for x in range(len(i) - 1):
            if i.count(i[x:x+2]) > 1:
                pairs = True

        for x in range(len(i) - 2):
            if i[x] == i[x+2]:
                gap = True

        if pairs == True and gap == True:
            nice += 1

    return nice

def main():
    puzzle_input = util.read.as_lines()

    nice = solve(puzzle_input)

    print("The number of nice strings is " + str(nice) + ".")

class AOC_Tests(unittest.TestCase):
    def test_ex1(self):
        return self.assertEqual(solve(["qjhvhtzxzqqjkmpb"]), 1)

    def test_ex2(self):
        return self.assertEqual(solve(["xxyxx"]), 1)

    def test_ex3(self):
        return self.assertEqual(solve(["uurcxstgmygtbstg"]), 0)

    def test_ex4(self):
        return self.assertEqual(solve(["ieodomkazucvgmuy"]), 0)

run(main)
