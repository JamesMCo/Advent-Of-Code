#!/usr/bin/env python3

#Advent of Code
#2019 Day 6, Part 2
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

        def path_to_com(self):
            node = self
            path = []
            while node.name != "COM":
                node = objs[node.parent]
                path.append(node.name)
            return path

    for o in puzzle_input:
        objs[o.split(")")[1]] = Tree(o)
    objs["COM"] = Tree("NULL)COM")

    a = objs["YOU"].path_to_com()
    for i, candidate in enumerate(objs["SAN"].path_to_com()):
        if candidate in a:
            return i + a.index(candidate)

def main():
    puzzle_input = util.read.as_lines()

    orbits = solve(puzzle_input)

    print("The minimum number of orbital transfers required to reach the object SAN is orbiting is " + str(orbits) + ".")

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
                                "K)L",
                                "K)YOU",
                                "I)SAN"]), 4)

if __name__ == "__main__":
    run(main)
