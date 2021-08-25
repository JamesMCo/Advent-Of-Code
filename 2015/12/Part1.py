#!/usr/bin/env python3

#Advent of Code
#2015 Day 12, Part 1
#Solution by James C. (https://github.com/JamesMCo)

import os, sys
sys.path.append(os.path.abspath("../.."))
import unittest, util.read
from util.tests import run

def solve(puzzle_input):
    total = 0

    puzzle_input = puzzle_input.replace("[", ",").replace("]", ",")
    puzzle_input = puzzle_input.replace("{", ",").replace("}", ",")
    puzzle_input = puzzle_input.replace(":", ",").replace(";", ",")

    for i in puzzle_input.split(","):
        try:
            total += int(i)
        except ValueError:
            pass

    return total

def main():
    puzzle_input = util.read.as_string()

    total = solve(puzzle_input)

    print("The final total is " + str(total) + ".")

class AOC_Tests(unittest.TestCase):
    def test_ex1(self):
        return self.assertEqual(solve("[1,2,3]"), 6)

    def test_ex2(self):
        return self.assertEqual(solve("{\"a\":2,\"b\":4}"), 6)

    def test_ex3(self):
        return self.assertEqual(solve("[[[3]]]"), 3)

    def test_ex4(self):
        return self.assertEqual(solve("{\"a\":{\"b\":4},\"c\":-1}"), 3)

    def test_ex5(self):
        return self.assertEqual(solve("{\"a\":[-1,1]}"), 0)

    def test_ex6(self):
        return self.assertEqual(solve("[-1,{\"a\":1}]"), 0)

    def test_ex7(self):
        return self.assertEqual(solve("[]"), 0)

    def test_ex8(self):
        return self.assertEqual(solve("{}"), 0)

run(main)
