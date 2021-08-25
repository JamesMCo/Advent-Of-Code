#!/usr/bin/env python3

#Advent of Code
#2015 Day 2, Part 2
#Solution by James C. (https://github.com/JamesMCo)

import os, sys
sys.path.append(os.path.abspath("../.."))
import unittest, util.read
from util.tests import run

def solve(puzzle_input):
    current = [[0, 0], [0, 0]]
    houses = set(["00"])
    santa = 0

    for i in puzzle_input:
        if   i == "^":
            current[santa][1] += 1
        elif i == ">":
            current[santa][0] += 1
        elif i == "v":
            current[santa][1] -= 1
        else:
            current[santa][0] -= 1

        houses.add(str(current[santa][0])+str(current[santa][1]))

        if santa == 0:
            santa = 1
        else:
            santa = 0

    return len(houses)

def main():
    puzzle_input = util.read.as_string()

    houses = solve(puzzle_input)

    print("The number of houses that will receive at least one present is " + str(houses) + ".")

class AOC_Tests(unittest.TestCase):
    def test_ex1(self):
        return self.assertEqual(solve("^v"), 3)

    def test_ex2(self):
        return self.assertEqual(solve("^>v<"), 3)

    def test_ex3(self):
        return self.assertEqual(solve("^v^v^v^v^v"), 11)

run(main)
