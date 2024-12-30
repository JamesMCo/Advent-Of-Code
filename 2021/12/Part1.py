#!/usr/bin/env python3

#Advent of Code
#2021 Day 12, Part 1
#Solution by James C. (https://github.com/JamesMCo)

import os, sys
sys.path.append(os.path.abspath("../.."))
import unittest, util.read
from util.tests import run

import networkx as nx

def solve(puzzle_input):
    graph = nx.Graph()
    graph.add_edges_from([line.split("-") for line in puzzle_input])

    def traverse(node, path=[]):
        if node == "end":
            return 1
        elif node.isupper() or (node.islower() and node not in path):
            return sum([traverse(child, path + [node]) for child in graph.neighbors(node)])
        else:
            return 0

    return traverse("start")

def main():
    puzzle_input = util.read.as_lines()

    paths = solve(puzzle_input)

    print("The number of paths that visit small caves at most once is " + str(paths) + ".")

class AOC_Tests(unittest.TestCase):
    def test_ex1(self):
        return self.assertEqual(solve(["start-A",
                                       "start-b",
                                       "A-c",
                                       "A-b",
                                       "b-d",
                                       "A-end",
                                       "b-end"]), 10)

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
                                       "kj-dc"]), 19)

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
                                       "start-RW"]), 226)

if __name__ == "__main__":
    run(main)
