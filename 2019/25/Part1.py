#!/usr/bin/env python3

#Advent of Code
#2019 Day 25, Part 1
#Solution by James C. (https://github.com/JamesMCo)

import os, sys
sys.path.append(os.path.abspath("../.."))
import unittest, util.read
from util.tests import run

from copy import deepcopy
from itertools import combinations, chain
import networkx as nx
from util.intcode_2019 import IntcodeComputer

def solve(puzzle_input):
    # Overall strategy:
    # DFS-search the entire map
    #  (when exploring a child room, use a snapshot of the computer, and then when done discard that snapshot and revert to the original computer)
    #  (this makes the recursive DFS slightly easier, as we don't persist state from children to parents)
    # Determine which items are safe to take (won't halt the computer, and won't infinite loop/reject all further input)
    #  (create a snapshot of the computer, then take the item, then observe its state and behaviour when trying to move)
    # Using a reset machine:
    #  Navigate to all rooms with items and take the item(s) in those rooms
    #  Navigate to the Security Checkpoint and drop all items on the floor
    #  Take all subsets of items of all lengths
    #   (uses a snapshot to revert state to all items being on the floor again)
    #  Navigate to the Pressure-Sensitive Floor
    #   If the computer halts, parse its last line of output for the password
    #   Otherwise, try again with the next subset of items

    class Snapshot:
        computer: IntcodeComputer

        def __init__(self, original_computer: IntcodeComputer) -> None:
            self.original_computer = original_computer

        def __enter__(self):
            return deepcopy(self.original_computer)

        def __exit__(self, exc_type, exc_val, exc_tb):
            return False

    computer = IntcodeComputer().load_memory(puzzle_input)
    while not computer.waiting_for_input():
        computer.step()

    def parse_room(lines):
        name = ""
        doors = []
        items = []

        reading_doors = False
        reading_items = False
        for line in lines:
            if line.startswith("=="):
                if name == "":
                    name = line[3:-3]
                else:
                    # Getting information about a new room (i.e. Pressure-Sensitive Floor)
                    # Need to stop saving new data to not overwrite existing data
                    break
            elif line == "Doors here lead:":
                reading_doors = True
            elif line == "Items here:":
                reading_items = True
            elif line == "":
                reading_doors = False
                reading_items = False
            elif reading_doors:
                doors.append(line[2:])
            elif reading_items:
                items.append(line[2:])

        return name, doors, items

    def safe_to_take(item_name, doors, intcode_computer):
        with Snapshot(intcode_computer) as snapshot:
            while not snapshot.waiting_for_input():
                snapshot.step()
            snapshot.outputs.clear()
            snapshot.queue_inputs(f"take {item_name}\n")

            for step in range(10000):
                # Quite possibly a better cutoff point, but this output sensible results
                # (catching both halts and infinite loops)
                snapshot.step()
                if snapshot.halted:
                    return False
                elif snapshot.waiting_for_input():
                    break
            if not snapshot.waiting_for_input():
                return False

            # Check that we can still move after having taken the item
            snapshot.queue_inputs(doors[0] + "\n")
            while not snapshot.waiting_for_input():
                snapshot.step()
            return "==" in "".join(map(chr, snapshot.outputs))

    def get_room(direction, intcode_computer):
        intcode_computer.outputs.clear()
        with Snapshot(intcode_computer) as snapshot:
            snapshot.queue_inputs(f"{direction}\n")
            while not snapshot.waiting_for_input():
                snapshot.step()
            return parse_room("".join(map(chr, snapshot.outputs)).split("\n")), snapshot

    def explore_room(parent, intcode_computer):
        name, doors, items = parent
        for door in doors:
            child, child_snapshot = get_room(door, intcode_computer)
            if not graph.has_edge(name, child[0]) and name != child[0]:
                graph.add_edge(name, child[0])
                graph.nodes[name][child[0]] = door
                match door:
                    case "north": graph.nodes[child[0]][name] = "south"
                    case "south": graph.nodes[child[0]][name] = "north"
                    case "east":  graph.nodes[child[0]][name] = "west"
                    case "west":  graph.nodes[child[0]][name] = "east"
                if child[0] != "Pressure-Sensitive Floor":
                    # Only child of Pressure-Sensitive Floor is the Security Checkpoint
                    # Not having the right items, such as during the exploration phase,
                    # results in us being ejected from the room
                    explore_room(child, child_snapshot)
        item_locations[name] = []
        for item in items:
            if safe_to_take(item, doors, intcode_computer):
                item_locations[name].append(item)

    graph = nx.Graph()
    item_locations = {}

    # Find all rooms and safe items
    starting_room = parse_room("".join(map(chr, computer.outputs)).split("\n"))
    explore_room(starting_room, computer)
    shortest_paths = dict(nx.all_pairs_shortest_path(graph))

    # Navigate to each room, take its item(s), and take them to the Security Checkpoint
    current_room = starting_room[0]

    def find_path_to_location(source, target):
        path = []
        for before, after in zip(shortest_paths[source][target][:-1], shortest_paths[source][target][1:]):
            path.append(graph.nodes[before][after])
        return path

    for room in item_locations:
        if item_locations[room]:
            computer\
                .queue_inputs("\n".join(find_path_to_location(current_room, room)) + "\n")\
                .queue_inputs("\n".join(f"take {item}" for item in item_locations[room]) + "\n")
            current_room = room
    if current_room != "Security Checkpoint":
        computer.queue_inputs("\n".join(find_path_to_location(current_room, "Security Checkpoint")) + "\n")
        current_room = "Security Checkpoint"

    items = list(chain.from_iterable(item_locations.values()))
    computer.queue_inputs("\n".join(f"drop {item}" for item in items) + "\n")
    while not computer.waiting_for_input():
        computer.step()

    computer.outputs.clear()

    # Try all combinations of items
    for count in range(len(items) + 1):
        for inv in combinations(items, count):
            with Snapshot(computer) as snapshot:
                if inv:
                    snapshot.queue_inputs(("\n".join(f"take {item}" for item in inv) + "\n"))
                snapshot.queue_inputs(graph.nodes[current_room]["Pressure-Sensitive Floor"] + "\n")
                while True:
                    if snapshot.waiting_for_input():
                        break
                    elif snapshot.halted:
                        last_line = "".join(map(chr, snapshot.outputs)).strip().split("\n")[-1]
                        password = [word for word in last_line.split() if word.isnumeric()][0]
                        return int(password)
                    snapshot.step()

def main():
    puzzle_input = util.read.as_int_list(",")

    password = solve(puzzle_input)

    print("The password for the main airlock is " + str(password) + ".")

class AOC_Tests(unittest.TestCase):
    @unittest.skip("No test cases")
    def test_ex1(self):
        pass

run(main)
