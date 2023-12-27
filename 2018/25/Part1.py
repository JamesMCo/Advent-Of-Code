#!/usr/bin/env python3

#Advent of Code
#2018 Day 25, Part 1
#Solution by James C. (https://github.com/JamesMCo)

import os, sys
sys.path.append(os.path.abspath("../.."))
import unittest, util.read
from util.tests import run

from itertools import combinations
import networkx as nx

def solve(puzzle_input):
    graph = nx.Graph()

    for a, b in combinations((tuple(map(int, line.strip().split(","))) for line in puzzle_input), 2):
        graph.add_nodes_from((a, b))
        if sum(abs(a_val - b_val) for a_val, b_val in zip(a, b)) <= 3:
            graph.add_edge(a, b)

    return nx.number_connected_components(graph)

def main():
    puzzle_input = util.read.as_lines()

    constellations = solve(puzzle_input)

    print("The number of constellations is " + str(constellations) + ".")

class AOC_Tests(unittest.TestCase):
    def test_ex1(self):
        self.assertEqual(solve([" 0,0,0,0",
                                " 3,0,0,0",
                                " 0,3,0,0",
                                " 0,0,3,0",
                                " 0,0,0,3",
                                " 0,0,0,6",
                                " 9,0,0,0",
                                "12,0,0,0"]), 2)

    def test_ex2(self):
        self.assertEqual(solve(["-1,2,2,0",
                                "0,0,2,-2",
                                "0,0,0,-2",
                                "-1,2,0,0",
                                "-2,-2,-2,2",
                                "3,0,2,-1",
                                "-1,3,2,2",
                                "-1,0,-1,0",
                                "0,2,1,-2",
                                "3,0,0,0"]), 4)

    def test_ex3(self):
        self.assertEqual(solve(["1,-1,0,1",
                                "2,0,-1,0",
                                "3,2,-1,0",
                                "0,0,3,1",
                                "0,0,-1,-1",
                                "2,3,-2,0",
                                "-2,2,0,0",
                                "2,-2,0,-1",
                                "1,-1,0,-1",
                                "3,2,0,2"]), 3)

    def test_ex4(self):
        self.assertEqual(solve(["1,-1,-1,-2",
                                "-2,-2,0,1",
                                "0,2,1,3",
                                "-2,3,-2,1",
                                "0,2,3,-2",
                                "-1,-1,1,-2",
                                "0,-2,-1,0",
                                "-2,2,3,-1",
                                "1,2,2,0",
                                "-1,-2,0,-2"]), 8)

run(main)
