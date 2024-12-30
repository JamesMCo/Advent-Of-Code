#!/usr/bin/env python3

#Advent of Code
#2018 Day 22, Part 2
#Solution by /u/korylprince (https://www.reddit.com/r/adventofcode/comments/a8i1cy/2018_day_22_solutions/ecazvbe/)
#Implementation by James C. (https://github.com/JamesMCo)
#Damnit, I really need to look into how to use networkx myself.

import os, sys
sys.path.append(os.path.abspath("../.."))
import unittest, util.read
from util.tests import run

import networkx as nx

def solve(puzzle_input):
    depth = int(puzzle_input[0].split()[1])
    target_x, target_y = [int(x) for x in puzzle_input[1].split()[1].split(",")]
    
    g_indices = {}
    g_indices["0,0"] = 0
    g_indices[f"{target_x},{target_y}"] = 0
    coord_types = {}

    def geologic_index(x, y):
        if f"{x},{y}" in g_indices:
            return g_indices[f"{x},{y}"]
        elif y == 0:
            g_indices[f"{x},{y}"] = x * 16807
            return g_indices[f"{x},{y}"]
        elif x == 0:
            g_indices[f"{x},{y}"] = y * 48271
            return g_indices[f"{x},{y}"]
        else:
            g_indices[f"{x},{y}"] = erosion_level(x-1, y) * erosion_level(x, y-1)
            return g_indices[f"{x},{y}"]

    def erosion_level(x, y):
        return (geologic_index(x, y) + depth) % 20183

    def coord_type(x, y):
        if f"{x},{y}" in coord_types:
            return coord_types[f"{x},{y}"]
        else:
            coord_types[f"{x},{y}"] = ["rocky", "wet", "narrow"][erosion_level(x, y) % 3]
            return coord_types[f"{x},{y}"]

    def shortest_path():
        g = nx.Graph()
        for x in range(0, target_x+100):
            for y in range(0, target_y+100):
                items = {"rocky":  ["climb", "torch"],
                         "wet":    ["climb", "empty"],
                         "narrow": ["torch", "empty"]}[coord_type(x, y)]
                g.add_edge(f"{x},{y},{items[0]}", f"{x},{y},{items[1]}", weight=7)
                for offset in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                    if 0 <= x+offset[0] and 0 <= y+offset[1]:
                        neighbour_items = {"rocky":  ["climb", "torch"],
                                           "wet":    ["climb", "empty"],
                                           "narrow": ["torch", "empty"]}[coord_type(x+offset[0], y+offset[1])]
                        for item in set(items).intersection(set(neighbour_items)):
                            g.add_edge(f"{x},{y},{item}", f"{x+offset[0]},{y+offset[1]},{item}", weight=1)
        return nx.dijkstra_path_length(g, "0,0,torch", f"{target_x},{target_y},torch")

    return shortest_path()

def main():
    puzzle_input = util.read.as_lines()

    minutes = solve(puzzle_input)

    print("The fewest number of minutes you can take to reach the target is " + str(minutes) + ".")

class AOC_Tests(unittest.TestCase):
    def test_ex1(self):
        self.assertEqual(solve(["depth: 510",
                                "target: 10,10"]), 45)

if __name__ == "__main__":
    run(main)
