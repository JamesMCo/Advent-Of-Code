#!/usr/bin/env python3

#Advent of Code
#2016 Day 2, Part 2
#Solution by James C. (https://github.com/JamesMCo)

import os, sys
sys.path.append(os.path.abspath("../.."))
import unittest, util.read
from util.tests import run

def solve(puzzle_input):
    here = [0, 2]
    buttons = [[None, None, 5, None, None],
               [None, 2,    6, "A",  None],
               [1,    3,    7, "B",  "D" ],
               [None, 4,    8, "C",  None],
               [None, None, 9, None, None]]
    code = ""

    for l in puzzle_input:
        if l == "": continue
        for d in l:
            if d == "U" and here[1] != 0 and buttons[here[0]][here[1] - 1] != None:
                here[1] -= 1
            elif d == "D" and here[1] != 4 and buttons[here[0]][here[1] + 1] != None:
                here[1] += 1
            elif d == "L" and here[0] != 0 and buttons[here[0] - 1][here[1]] != None:
                here[0] -= 1
            elif d == "R" and here[0] != 4 and buttons[here[0] + 1][here[1]] != None:
                here[0] += 1
        code += str(buttons[here[0]][here[1]])

    return code

def main():
    puzzle_input = util.read.as_lines()

    code = solve(puzzle_input)

    print("The code for the bathroom is " + str(code) + ".")

class AOC_Tests(unittest.TestCase):
    def test_ex1(self):
        self.assertEqual(solve(["ULL",
                                "RRDDD",
                                "LURDL",
                                "UUUUD"]), "5DB3")

if __name__ == "__main__":
    run(main)
