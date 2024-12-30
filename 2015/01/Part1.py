#!/usr/bin/env python3

#Advent of Code
#2015 Day 1, Part 1
#Solution by James C. (https://github.com/JamesMCo)

import os, sys
sys.path.append(os.path.abspath("../.."))
import unittest, util.read
from util.tests import run

def solve(puzzle_input):
    floor = 0

    for i in puzzle_input:
        if i == "(":
            floor += 1
        else:
            floor -= 1

    return floor

def main():
    puzzle_input = util.read.as_string()

    floor = solve(puzzle_input)

    print("Santa's instructions take him to floor " + str(floor) + ".")

class AOC_Tests(unittest.TestCase):
    def test_ex1(self):
        return self.assertEqual(solve("(())"), 0)

    def test_ex2(self):
        return self.assertEqual(solve("()()"), 0)

    def test_ex3(self):
        return self.assertEqual(solve("((("), 3)

    def test_ex4(self):
        return self.assertEqual(solve("(()(()("), 3)

    def test_ex5(self):
        return self.assertEqual(solve("))((((("), 3)

    def test_ex6(self):
        return self.assertEqual(solve("())"), -1)

    def test_ex7(self):
        return self.assertEqual(solve("))("), -1)

    def test_ex8(self):
        return self.assertEqual(solve(")))"), -3)

    def test_ex9(self):
        return self.assertEqual(solve(")())())"), -3)

if __name__ == "__main__":
    run(main)
