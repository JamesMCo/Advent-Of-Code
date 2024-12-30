#!/usr/bin/env python3

#Advent of Code
#2016 Day 9, Part 2
#Solution by /u/rhardih (https://reddit.com/r/adventofcode/comments/5hbygy/-/dazentu/)
#Implementation by James C. (https://github.com/JamesMCo)
#Gosh darn, I'm annoyed I couldn't figure out a solution myself :(

import os, sys
sys.path.append(os.path.abspath("../.."))
import unittest, util.read
from util.tests import run

def solve(puzzle_input):
    weights = [1 for i in puzzle_input]
    length = 0
    i = 0
    while i < len(puzzle_input):
        if puzzle_input[i] == "(":
            l = int(puzzle_input[i+1:].split("x")[0])
            r = int(puzzle_input[i+1:].split("x")[1].split(")")[0])
            for x in range(i+len(str(l))+len(str(r))+3, i+len(str(l))+len(str(r))+l+3):
                weights[x] = weights[x] * r
            i += len(str(l))+len(str(r))+3
        else:
            length += weights[i]
            i += 1
    return length

def main():
    puzzle_input = util.read.as_string().replace(" ", "")

    l = solve(puzzle_input)

    print("The decompressed length of the file is " + str(l) + ".")

class AOC_Tests(unittest.TestCase):
    def test_ex1(self):
        self.assertEqual(solve("(3x3)XYZ"), 9)
        
    def test_ex2(self):
        self.assertEqual(solve("X(8x2)(3x3)ABCY"), 20)
        
    def test_ex3(self):
        self.assertEqual(solve("(27x12)(20x12)(13x14)(7x10)(1x12)A"), 241920)
        
    def test_ex4(self):
        self.assertEqual(solve("(25x3)(3x3)ABC(2x3)XY(5x2)PQRSTX(18x9)(3x2)TWO(5x7)SEVEN"), 445)

if __name__ == "__main__":
    run(main)
