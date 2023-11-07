#!/usr/bin/env python3

#Advent of Code
#2019 Day 15, Part 1, Animated
#Solution by James C. (https://github.com/JamesMCo)

import os, sys
sys.path.append(os.path.abspath("../.."))
import util.read

from math import inf
import networkx as nx
from time import sleep
from util.two_d_world import World
from util.intcode_2019 import IntcodeComputer

puzzle_input = util.read.as_int_list(",")
i = IntcodeComputer().load_memory(puzzle_input)


def display_cell(cell):
    if cell == -1:
        return " "
    else:
        return cell

def pprint(map_of_area, x, y):
    os.system("cls" if os.name == "nt" else "clear")
    before = map_of_area[(x, y)]
    map_of_area[(x, y)] = "D"
    print(map_of_area.pprint_custom(" ", display_cell))
    map_of_area[(x, y)] = before
    sleep(0.016)

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
path_to_target = {}
computer.register_output_listener(lambda val: pprint(area, *path_to_target[len(computer.outputs) - 1 if val == 0 else len(computer.outputs)]))

for neighbour in neighbours(0, 0):
    area_graph.add_edge((0, 0), neighbour, weight=1_000_000_000)
    unexplored.add(neighbour)

droid_x, droid_y = (0, 0)
oxygen = None

while unexplored:
    target = nearest_unexplored(unexplored, area_graph, droid_x, droid_y)
    path_to_target = nx.shortest_path(area_graph, (droid_x, droid_y), target)

    computer.queue_inputs(
        direction_between_cells(*start, *end) for start, end in zip(path_to_target, path_to_target[1:]))
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
                area[target] = "O"
                oxygen = target

    area.min_x = min(droid_x - 1, area.min_x)
    area.min_y = min(droid_y - 1, area.min_y)
    area.max_x = max(droid_x + 1, area.max_x)
    area.max_y = max(droid_y + 1, area.max_y)

    computer.outputs.clear()

pprint(area, droid_x, droid_y)