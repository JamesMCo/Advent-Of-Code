#!/usr/bin/env python3

#Advent of Code
#2021 Day 13, Part 1
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

    paper.load_from_dict({coord: "#" for coord in fold(paper, *folds[0])})

    return len(paper.keys())

def main():
    puzzle_input = util.read.as_lines()

    dots = solve(puzzle_input)

    print("The number of dots that are visible after the first fold instruction is " + str(dots) + ".")

class AOC_Tests(unittest.TestCase):
    def test_ex1(self):
        return self.assertEqual(solve(["6,10",
                                       "0,14",
                                       "9,10",
                                       "0,3",
                                       "10,4",
                                       "4,11",
                                       "6,0",
                                       "6,12",
                                       "4,1",
                                       "0,13",
                                       "10,12",
                                       "3,4",
                                       "3,0",
                                       "8,4",
                                       "1,10",
                                       "2,14",
                                       "8,10",
                                       "9,0",
                                       "",
                                       "fold along y=7",
                                       "fold along x=5"]), 17)

if __name__ == "__main__":
    run(main)
