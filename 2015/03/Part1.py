#!/usr/bin/env python3

#Advent of Code
#2015 Day 3, Part 1
#Solution by James C. (https://github.com/JamesMCo)

import os, sys
sys.path.append(os.path.abspath("../.."))
import unittest, util.read
from util.tests import run

def solve(puzzle_input):
    current = [0, 0]
    houses = set(["00"])

    for i in puzzle_input:
        if   i == "^":
            current[1] += 1
        elif i == ">":
            current[0] += 1
        elif i == "v":
            current[1] -= 1
        else:
            current[0] -= 1

        houses.add(str(current[0])+str(current[1]))

    return len(houses)

def main():
    puzzle_input = util.read.as_string()

    houses = solve(puzzle_input)

    print("The number of houses that will receive at least one present is " + str(houses) + ".")

class AOC_Tests(unittest.TestCase):
    def test_ex1(self):
        return self.assertEqual(solve(">"), 2)

    def test_ex2(self):
        return self.assertEqual(solve("^>v<"), 4)

    def test_ex3(self):
        return self.assertEqual(solve("^v^v^v^v^v"), 2)

if __name__ == "__main__":
    run(main)
