#!/usr/bin/env python3

#Advent of Code
#2019 Day 6, Part 1
#Solution by James C. (https://github.com/JamesMCo)

import os, sys
sys.path.append(os.path.abspath("../.."))
import unittest, util.read
from util.tests import run

def solve(puzzle_input):
    objs = {}

    class Tree:
        def __init__(self, description):
            self.parent, self.name = description.split(")")

        def calc_orbits(self):
            orbits = 0
            node = self
            while node.name != "COM":
                node = objs[node.parent]
                orbits += 1
            return orbits

    for o in puzzle_input:
        objs[o.split(")")[1]] = Tree(o)
    objs["COM"] = Tree("NULL)COM")

    return sum(o.calc_orbits() for o in objs.values())

def main():
    puzzle_input = util.read.as_lines()

    orbits = solve(puzzle_input)

    print("The total number of direct and indirect orbits is " + str(orbits) + ".")

class AOC_Tests(unittest.TestCase):
    def test_ex1(self):
        self.assertEqual(solve(["COM)B",
                                "B)C",
                                "C)D",
                                "D)E",
                                "E)F",
                                "B)G",
                                "G)H",
                                "D)I",
                                "E)J",
                                "J)K",
                                "K)L"]), 42)

run(main)
