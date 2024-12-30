#!/usr/bin/env python3

#Advent of Code
#2023 Day 25, Part 1
#Solution by James C. (https://github.com/JamesMCo)

import os, sys
sys.path.append(os.path.abspath("../.."))
import unittest, util.read
from util.tests import run

from collections import defaultdict
from itertools import combinations
import networkx as nx

def solve(puzzle_input: list[str]) -> int:
    graph = nx.Graph()
    for line in puzzle_input:
        line = line.split()
        source = line[0][:-1]
        for dest in line[1:]:
            graph.add_edge(source, dest)

    # Edges that need to be cut are probably traversed a lot in shortest paths
    # Use that as a method to sort edges, then use itertools.combinations
    # to select three different edges at a time and see if they disconnect
    # the graphs.

    paths = dict(nx.all_pairs_shortest_path(graph))
    times_traversed = defaultdict(int)
    for source in paths:
        for dest in paths[source]:
            for edge in zip(paths[source][dest][:-1], paths[source][dest][1:]):
                times_traversed[tuple(sorted(edge))] += 1

    for disconnected in combinations(sorted(times_traversed, key=times_traversed.get, reverse=True), 3):
        new_graph = graph.edge_subgraph((edge for edge in graph.edges if tuple(sorted(edge)) not in disconnected))
        if not nx.has_path(new_graph, disconnected[0][0], disconnected[0][1]):
            return len(nx.single_source_shortest_path(new_graph, disconnected[0][0])) * len(nx.single_source_shortest_path(new_graph, disconnected[0][1]))

def main() -> tuple[str, int]:
    puzzle_input = util.read.as_lines()

    return "The product of the sizes of the two groups is {}.", solve(puzzle_input)

class AOC_Tests(unittest.TestCase):
    def test_ex1(self):
        return self.assertEqual(solve(["jqt: rhn xhk nvd",
                                       "rsh: frs pzl lsr",
                                       "xhk: hfx",
                                       "cmg: qnr nvd lhk bvb",
                                       "rhn: xhk bvb hfx",
                                       "bvb: xhk hfx",
                                       "pzl: lsr hfx nvd",
                                       "qnr: nvd",
                                       "ntq: jqt hfx bvb xhk",
                                       "nvd: lhk",
                                       "lsr: lhk",
                                       "rzs: qnr cmg lsr rsh",
                                       "frs: qnr lhk lsr"]), 54)

if __name__ == "__main__":
    run(main)
