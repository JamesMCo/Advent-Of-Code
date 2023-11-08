#!/usr/bin/env python3

#Advent of Code
#2019 Day 15, Part 2
#Solution by James C. (https://github.com/JamesMCo)

import os, sys
sys.path.append(os.path.abspath("../.."))
import unittest, util.read
from util.tests import run

from math import inf
import networkx as nx
from util.two_d_world import World
from util.intcode_2019 import IntcodeComputer

def solve(puzzle_input):
    def neighbours(x, y):
        yield from [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)]

    def nearest_unexplored(unexplored_cells, graph, current_x, current_y):
        path_lengths = nx.single_source_shortest_path_length(graph, (current_x, current_y))
        return min(unexplored_cells, key=lambda cell: path_lengths[cell] if (current_x, current_y) != cell else inf)

    def direction_between_cells(start_x, start_y, end_x, end_y):
        if (start_x, start_y) == (end_x, end_y):
            raise ValueError("No valid direction between same start and end cell")

        if start_y > end_y:
            # Moving up - north
            return 1
        elif start_y < end_y:
            # Moving down - south
            return 2
        elif start_x > end_x:
            # Moving left - west
            return 3
        elif start_x < end_x:
            # Moving right - west
            return 4

    computer = IntcodeComputer().load_memory(puzzle_input)
    area = World(-1, True)
    area_graph = nx.Graph()
    unexplored = {(0, 0)}

    for neighbour in neighbours(0, 0):
        area_graph.add_edge((0, 0), neighbour, weight=1_000_000_000)
        unexplored.add(neighbour)

    droid_x, droid_y = (0, 0)
    oxygen = None

    while unexplored:
        target = nearest_unexplored(unexplored, area_graph, droid_x, droid_y)
        path_to_target = nx.shortest_path(area_graph, (droid_x, droid_y), target)

        computer.queue_inputs(direction_between_cells(*start, *end) for start, end in zip(path_to_target, path_to_target[1:]))
        while len(computer.outputs) != len(path_to_target) - 1:
            computer.step()

        match computer.outputs[-1]:
            case 0:
                # "The repair droid hit a wall. Its position has not changed."
                area[target] = "#"
                area_graph.remove_node(target)
                unexplored.remove(target)
                droid_x, droid_y = path_to_target[-2]
            case 1 | 2:
                # "The repair droid has moved one step in the requested direction."
                area[target] = "."
                for neighbour in neighbours(*target):
                    match area[neighbour]:
                        case -1:
                            area_graph.add_edge(target, neighbour, weight=1_000_000_000)
                            unexplored.add(neighbour)
                        case ".":
                            area_graph.add_edge(target, neighbour, weight=1)
                unexplored.remove(target)
                droid_x, droid_y = target

                if computer.outputs[-1] == 2:
                    # "The repair droid has moved one step in the requested direction; its new position is the location of the oxygen system."
                    oxygen = target
        computer.outputs.clear()

    return max(nx.single_source_shortest_path_length(area_graph, oxygen).values())

def main():
    puzzle_input = util.read.as_int_list(",")

    minutes = solve(puzzle_input)

    print("The number of minutes it will take to fill with oxygen is " + str(minutes) + ".")

class AOC_Tests(unittest.TestCase):
    @unittest.skip("No test cases")
    def test_ex1(self):
        pass

run(main)
