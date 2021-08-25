#!/usr/bin/env python3

#Advent of Code
#2015 Day 16, Part 1
#Solution by James C. (https://github.com/JamesMCo)

import os, sys
sys.path.append(os.path.abspath("../.."))
import unittest, util.read
from util.tests import run

def solve(puzzle_input):
    data = {
        "children": 3,
        "cats": 7,
        "samoyeds": 2,
        "pomeranians": 3,
        "akitas": 0,
        "vizslas": 0,
        "goldfish": 5,
        "trees": 3,
        "cars": 2,
        "perfumes": 1
    }

    sues = []
    for sue in puzzle_input:
        d = {}
        for i in range(2, len(sue.split()), 2):
            if sue.split()[i+1][-1] == ",":
                d[sue.split()[i][:-1]] = int(sue.split()[i+1][:-1])
            else:
                d[sue.split()[i][:-1]] = int(sue.split()[i+1])
        sues.append(d)

    for i, sue in enumerate(sues):
        found = True
        for d in sue:
            if sue[d] != data[d]:
                found = False
                break
        if found:
            return i+1

def main():
    puzzle_input = util.read.as_lines()

    sue = solve(puzzle_input)

    print("The number of the Sue that got the gift is " + str(sue) + ".")

class AOC_Tests(unittest.TestCase):
    @unittest.skip("No test cases")
    def test_ex1(self):
        pass

run(main)
