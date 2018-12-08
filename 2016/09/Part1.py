#!/usr/bin/env python3

#Advent of Code
#2016 Day 9, Part 1
#Solution by James C. (https://github.com/JamesMCo)

import os, sys
sys.path.append(os.path.abspath("../.."))
import unittest, util.read
from util.tests import run

def solve(puzzle_input):
    i = 0
    while i < len(puzzle_input):
        if puzzle_input[i] == "(":
            l = int(puzzle_input[i+1:].split("x")[0])
            r = int(puzzle_input[i+1:].split("x")[1].split(")")[0])
            puzzle_input = puzzle_input[:i] + ")".join(puzzle_input[i:].split(")")[1:])[:l] * r + ")".join(puzzle_input[i+1:].split(")")[1:])[l:]
            i += r*l
        else:
            i += 1

    return len(puzzle_input)

def main():
    puzzle_input = util.read.as_string().replace(" ", "")

    l = solve(puzzle_input)

    print("The decompressed length of the file is " + str(l) + ".")

class AOC_Tests(unittest.TestCase):
    def test_ex1(self):
        self.assertEqual(solve("ADVENT"), 6)
        
    def test_ex2(self):
        self.assertEqual(solve("A(1x5)BC"), 7)
        
    def test_ex3(self):
        self.assertEqual(solve("(3x3)XYZ"), 9)
        
    def test_ex4(self):
        self.assertEqual(solve("A(2x2)BCD(2x2)EFG"), 11)
        
    def test_ex5(self):
        self.assertEqual(solve("(6x1)(1x3)A"), 6)
        
    def test_ex6(self):
        self.assertEqual(solve("X(8x2)(3x3)ABCY"), 18)

run(main)
