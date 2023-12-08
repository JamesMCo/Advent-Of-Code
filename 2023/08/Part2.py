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
        # I'm not 100% sure that this would work for all inputs,
        # and I'm almost certain that it wouldn't work with a
        # general input, but it works for my input at the very least!

        instructions = cycle(zip(puzzle_input[0], range(len(puzzle_input[0]))))
        current_node = start_node
        seen = []
        while True:
            current_instruction, instruction_i = next(instructions)
            if (current_node, instruction_i) in seen:
                return len(seen) - seen.index((current_node, instruction_i))
            else:
                seen.append((current_node, instruction_i))
                current_node = graph.nodes[current_node][current_instruction]

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
