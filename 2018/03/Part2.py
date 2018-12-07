#!/usr/bin/env python3

#Advent of Code
#Day 3, Part 2
#Solution by James C. (https://github.com/JamesMCo)

import os, sys, colorama, time
sys.path.append(os.path.abspath("../.."))
import unittest, util.read
from util.tests import run

from collections import defaultdict

def solve(puzzle_input):
    fabric = defaultdict(int)

    for line in puzzle_input:
        left, top     = [int(x) for x in line.split()[2][:-1].split(",")]
        width, height = [int(x) for x in line.split()[3].split("x")]

        for x in range(left, left+width):
            for y in range(top, top+height):
                fabric[f"{x},{y}"] += 1

    for line in puzzle_input:
        left, top     = [int(x) for x in line.split()[2][:-1].split(",")]
        width, height = [int(x) for x in line.split()[3].split("x")]

        in_tact = True

        for x in range(left, left+width):
            for y in range(top, top+height):
                if fabric[f"{x},{y}"] > 1:
                    in_tact = False
                    break

        if in_tact:
            return int(line.split()[0][1:])

def main():
    puzzle_input = util.read.as_lines()

    claim_id = solve(puzzle_input)

    print("The id of the in tact claim is " + str(claim_id) + ".")

class AOC_Tests(unittest.TestCase):
    def test_ex1(self):
        self.assertEqual(solve(["#1 @ 1,3: 4x4",
                                "#2 @ 3,1: 4x4",
                                "#3 @ 5,5: 2x2"]), 3)

run(main)
