#!/usr/bin/env python3

#Advent of Code
#2023 Day 8, Part 2
#Solution by James C. (https://github.com/JamesMCo)

import os, sys
sys.path.append(os.path.abspath("../.."))
import unittest, util.read
from util.tests import run

from itertools import cycle
from math import lcm
import networkx as nx
import re

def solve(puzzle_input: list[str]) -> int:
    graph = nx.DiGraph()
    node_definition: re.Pattern = re.compile(r"([^ ]+) = \(([^ ]+), ([^ ]+)\)")

    for line in puzzle_input[2:]:
        node, left, right = node_definition.match(line).groups()
        graph.add_node(node, L=left, R=right)
        graph.add_edge(node, left)
        graph.add_edge(node, right)

    def find_cycle(start_node: str) -> int:
        # After reading through some discussions on the subreddit, I found that
        # more assumptions could be made about the graphs given as inputs:
        #
        # - The routes given by the inputs will always cycle
        # - The cycle will only contain one **Z node
        # - The cycle for a given **A node is not shared
        #   by any other **A node
        # - The length from the **A node to the **Z is the
        #   same as the length of **Z to **Z in the cycle
        #
        # These assumptions mean that the approach to finding the cycle is
        # simpler than I originally implemented. Instead, we can find the
        # number of steps needed to reach the **Z node and return that.
        # Obviously, this wouldn't work for any arbitrary graph, but for
        # those given as puzzle inputs, it should be fine.

        instructions = cycle(puzzle_input[0])
        current_node = start_node
        steps = 0
        while not current_node.endswith("Z"):
            current_node = graph.nodes[current_node][next(instructions)]
            steps += 1
        return steps

    return lcm(*map(find_cycle, filter(lambda n: n.endswith("A"), graph)))

def main() -> tuple[str, int]:
    puzzle_input = util.read.as_lines()

    return "The number of steps required to reach before all nodes end with Z is {}.", solve(puzzle_input)

class AOC_Tests(unittest.TestCase):
    def test_ex1(self):
        return self.assertEqual(solve(["LR",
                                       "",
                                       "11A = (11B, XXX)",
                                       "11B = (XXX, 11Z)",
                                       "11Z = (11B, XXX)",
                                       "22A = (22B, XXX)",
                                       "22B = (22C, 22C)",
                                       "22C = (22Z, 22Z)",
                                       "22Z = (22B, 22B)",
                                       "XXX = (XXX, XXX)"]), 6)

run(main)
