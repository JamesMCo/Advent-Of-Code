#!/usr/bin/env python3

#Advent of Code
#2023 Day 8, Part 1
#Solution by James C. (https://github.com/JamesMCo)

import os, sys
sys.path.append(os.path.abspath("../.."))
import unittest, util.read
from util.tests import run

from itertools import cycle
import networkx as nx
import re

def solve(puzzle_input: list[str]) -> int:
    instructions = cycle(puzzle_input[0])
    graph = nx.DiGraph()
    node_definition: re.Pattern = re.compile(r"([^ ]+) = \(([^ ]+), ([^ ]+)\)")

    for line in puzzle_input[2:]:
        node, left, right = node_definition.match(line).groups()
        graph.add_node(node, L=left, R=right)
        graph.add_edge(node, left)
        graph.add_edge(node, right)

    current_node = "AAA"
    steps = 0
    while current_node != "ZZZ":
        current_node = graph.nodes[current_node][next(instructions)]
        steps += 1
    return steps

def main() -> tuple[str, int]:
    puzzle_input = util.read.as_lines()

    return "The number of steps required to reach ZZZ is {}.", solve(puzzle_input)

class AOC_Tests(unittest.TestCase):
    def test_ex1(self):
        return self.assertEqual(solve(["RL",
                                       "",
                                       "AAA = (BBB, CCC)",
                                       "BBB = (DDD, EEE)",
                                       "CCC = (ZZZ, GGG)",
                                       "DDD = (DDD, DDD)",
                                       "EEE = (EEE, EEE)",
                                       "GGG = (GGG, GGG)",
                                       "ZZZ = (ZZZ, ZZZ)"]), 2)

    def test_ex2(self):
        return self.assertEqual(solve(["LLR",
                                       "",
                                       "AAA = (BBB, BBB)",
                                       "BBB = (AAA, ZZZ)",
                                       "ZZZ = (ZZZ, ZZZ)"]), 6)

run(main)
