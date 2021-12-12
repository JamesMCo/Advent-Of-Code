#!/usr/bin/env python3

#Advent of Code
#2021 Day 12, Part 2
#Solution by James C. (https://github.com/JamesMCo)

import os, sys
sys.path.append(os.path.abspath("../.."))
import unittest, util.read
from util.tests import run

import networkx as nx

def solve(puzzle_input):
    graph = nx.Graph()
    graph.add_edges_from([line.split("-") for line in puzzle_input])

    def traverse(node, path=[], used_small_repeat=False):
        if node == "start" and node in path:
            return 0
        elif node == "end":
            return 1
        elif node.isupper() or (node.islower() and node not in path):
            return sum([traverse(child, path + [node], used_small_repeat) for child in graph.neighbors(node)])
        elif node.islower() and not used_small_repeat and path.count(node) == 1:
            return sum([traverse(child, path + [node], True) for child in graph.neighbors(node)])
        else:
            return 0

    return traverse("start")

def main():
    puzzle_input = util.read.as_lines()

    paths = solve(puzzle_input)

    print("The number of paths through the cave system is " + str(paths) + ".")

class AOC_Tests(unittest.TestCase):
    def test_ex1(self):
        return self.assertEqual(solve(["start-A",
                                       "start-b",
                                       "A-c",
                                       "A-b",
                                       "b-d",
                                       "A-end",
                                       "b-end"]), 36)

    def test_ex2(self):
        return self.assertEqual(solve(["dc-end",
                                       "HN-start",
                                       "start-kj",
                                       "dc-start",
                                       "dc-HN",
                                       "LN-dc",
                                       "HN-end",
                                       "kj-sa",
                                       "kj-HN",
                                       "kj-dc"]), 103)

    def test_ex3(self):
        return self.assertEqual(solve(["fs-end",
                                       "he-DX",
                                       "fs-he",
                                       "start-DX",
                                       "pj-DX",
                                       "end-zg",
                                       "zg-sl",
                                       "zg-pj",
                                       "pj-he",
                                       "RW-he",
                                       "fs-DX",
                                       "pj-RW",
                                       "zg-RW",
                                       "start-pj",
                                       "he-WI",
                                       "zg-he",
                                       "pj-fs",
                                       "start-RW"]), 3509)

run(main)
