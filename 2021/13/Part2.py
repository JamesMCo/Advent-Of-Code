#!/usr/bin/env python3

#Advent of Code
#2021 Day 13, Part 2
#Solution by James C. (https://github.com/JamesMCo)

import os, sys
sys.path.append(os.path.abspath("../.."))
import unittest, util.read
from util.tests import run

from itertools import dropwhile, takewhile
from util.two_d_world import World

def solve(puzzle_input):
    def fold(paper, axis, fold_line):
        new_coords = {}
        for x, y in paper.keys():
            if axis == "x" and x > fold_line:
                new_coords[(x - (2 * (x - fold_line)), y)] = "#"
            elif axis == "y" and y > fold_line:
                new_coords[(x, y - (2 * (y - fold_line)))] = "#"
            else:
                new_coords[(x, y)] = "#"
        return new_coords

    dots  = [tuple(int(n) for n in line.split(",")) for line in takewhile(lambda l: l != "", puzzle_input)]
    folds = [(line.split()[-1].split("=")[0], int(line.split()[-1].split("=")[1])) for line in dropwhile(lambda l: not l.startswith("fold"), puzzle_input)]

    paper = World(".", True)
    paper.load_from_dict({coord: "#" for coord in dots})

    for instruction in folds:
        paper.load_from_dict({coord: "#" for coord in fold(paper, *instruction)})

    return paper.pprint(" ", "█")

def main():
    puzzle_input = util.read.as_lines()

    paper = solve(puzzle_input)

    print("The code used to activate the infrared thermal imaging camera is:\n" + str(paper))

class AOC_Tests(unittest.TestCase):
    @unittest.skip("No test cases")
    def test_ex1(self):
        pass

if __name__ == "__main__":
    run(main)
