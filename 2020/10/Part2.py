#!/usr/bin/env python3

#Advent of Code
#2020 Day 10, Part 2
#Solution by James C. (https://github.com/JamesMCo)

import os, sys
sys.path.append(os.path.abspath("../.."))
import unittest, util.read
from util.tests import run

from functools import cache
import networkx as nx

def solve(puzzle_input):
    puzzle_input = [0] + sorted(puzzle_input) + [max(puzzle_input) + 3]

    graph = nx.DiGraph()

    for i in range(1, 4):
        for base, candidate in zip(puzzle_input, puzzle_input[i:]):
            if candidate - base <= 3:
                graph.add_edge(base, candidate)

    @cache
    def paths_out(node):
        if len(graph.succ[node]) == 0:
            return 1
        else:
            return sum(paths_out(child) for child in graph.succ[node])

    return paths_out(0)

def main():
    puzzle_input = util.read.as_int_list("\n")

    arrangements = solve(puzzle_input)

    print("The total number of distinct ways you can arrange the adapters is " + str(arrangements) + ".")

class AOC_Tests(unittest.TestCase):
    def test_ex1(self):
        return self.assertEqual(solve([16, 10, 15, 5, 1, 11, 7, 19, 6, 12, 4]), 8)

    def test_ex2(self):
        return self.assertEqual(solve([28, 33, 18, 42, 31, 14, 46, 20, 48, 47,
                                       24, 23, 49, 45, 19, 38, 39, 11,  1, 32,
                                       25, 35,  8, 17,  7,  9,  4,  2, 34, 10, 3]), 19208)

run(main)
