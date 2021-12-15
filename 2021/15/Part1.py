#!/usr/bin/env python3

#Advent of Code
#2021 Day 15, Part 1
#Solution by James C. (https://github.com/JamesMCo)

import os, sys
sys.path.append(os.path.abspath("../.."))
import unittest, util.read
from util.tests import run

import networkx as nx

def solve(puzzle_input):
    def neighbours(x, y):
        coords = [(x+dx, y+dy) for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)] if 0 <= (x+dx) < len(puzzle_input[0]) and 0 <= (y+dy) < len(puzzle_input)]
        for (n_x, n_y) in coords:
            yield (n_x, n_y), int(puzzle_input[n_y][n_x])

    graph = nx.DiGraph()
    for y, row in enumerate(puzzle_input):
        for x, col in enumerate(row):
            for neighbour, risk in neighbours(x, y):
                graph.add_edge((x, y), neighbour, weight=risk)

    return nx.dijkstra_path_length(graph, (0, 0), (len(puzzle_input[0])-1, len(puzzle_input)-1))

def main():
    puzzle_input = util.read.as_lines()

    risk = solve(puzzle_input)

    print("The lowest total risk of any path is " + str(risk) + ".")

class AOC_Tests(unittest.TestCase):
    def test_ex1(self):
        return self.assertEqual(solve(["1163751742",
                                       "1381373672",
                                       "2136511328",
                                       "3694931569",
                                       "7463417111",
                                       "1319128137",
                                       "1359912421",
                                       "3125421639",
                                       "1293138521",
                                       "2311944581"]), 40)

run(main)
