#!/usr/bin/env python3

#Advent of Code
#2022 Day 12, Part 2
#Solution by James C. (https://github.com/JamesMCo)

import os, sys
sys.path.append(os.path.abspath("../.."))
import unittest, util.read
from util.tests import run

import math
import networkx as nx

def solve(puzzle_input):
    height = len(puzzle_input)
    width  = len(puzzle_input[0])

    def parse_space(space):
        match space:
            case "S":
                return 0
            case "E":
                return 25
            case letter:
                return ord(letter) - ord("a")

    starts = []
    target = None
    for y, row in enumerate(puzzle_input):
        for x, col in enumerate(row):
            if col in "Sa":
                starts.append((x, y))
            if col == "E":
                target = (x, y)

    puzzle_input = [[parse_space(space) for space in row] for row in puzzle_input]

    def neighbours(x, y):
        # Returns in order up, right, down, left
        if y != 0:
            yield ((x, y - 1), puzzle_input[y - 1][x])
        if x != width - 1:
            yield ((x + 1, y), puzzle_input[y][x + 1])
        if y != height - 1:
            yield ((x, y + 1), puzzle_input[y + 1][x])
        if x != 0:
            yield ((x - 1, y), puzzle_input[y][x - 1])

    heightmap_graph = nx.DiGraph()

    for y, row in enumerate(puzzle_input):
        for x, strength in enumerate(row):
            for neighbour, neighbour_strength in neighbours(x, y):
                if neighbour_strength <= strength + 1:
                    heightmap_graph.add_edge((x, y), neighbour)

    distance = math.inf
    for start in starts:
        try:
            distance = min(distance, nx.shortest_path_length(heightmap_graph, start, target))
        except nx.exception.NetworkXNoPath:
            # Not all starting locations are possible to reach the top from
            # (e.g. an area of "a"s surrounded on all sides by "c"s)
            pass
            
    return distance

def main():
    puzzle_input = util.read.as_lines()

    steps = solve(puzzle_input)

    print("The fewest steps required to reach the location with the best signal is " + str(steps) + ".")

class AOC_Tests(unittest.TestCase):
    def test_ex1(self):
        return self.assertEqual(solve(["Sabqponm",
                                       "abcryxxl",
                                       "accszExk",
                                       "acctuvwj",
                                       "abdefghi"]), 29)

run(main)
