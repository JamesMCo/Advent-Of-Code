#!/usr/bin/env python3

#Advent of Code
#2022 Day 16, Part 1
#Solution by James C. (https://github.com/JamesMCo)

import os, sys
sys.path.append(os.path.abspath("../.."))
import unittest, util.read
from util.tests import run

from functools import cache
import networkx as nx
import re

def solve(puzzle_input):
    # Originally solved in a slightly naïve way, but rewritten to be more efficient
    # after reading some comments on /r/adventofcode. Notably, instead of walking
    # the graph minute by minute, the only step that this version considers is
    # moving from one valve to another and opening it immediately. It also only
    # considers valves with a flow greater than 0.

    time_limit = 30

    g = nx.Graph()
    valves = {}
    for valve_description in puzzle_input:
        valve, flow, tunnels = re.match("Valve (\w+) has flow rate=(\d+); tunnels? leads? to valves? ((?:(?:, )?\w+)+)", valve_description).groups()
        if (flow := int(flow)) > 0:
            valves[valve] = flow
        for destination in tunnels.split(", "):
            g.add_edge(valve, destination)
    shortest_paths = {}
    for source, targets in nx.all_pairs_shortest_path_length(g):
        # All valves can be sources, just in case we end up at one
        # (i.e. Start at AA, AA has 0 flow)
        shortest_paths[source] = {}
        for target, distance in targets.items():
            if target in valves:
                # If target has greater than 0 flow
                shortest_paths[source][target] = distance + 1

    @cache
    def simulate(minute=1, location="AA", open_valves=frozenset()):
        # Minute      := int from 1 to 30
        # Location    := string name of valve in current room
        # Open valves := set of tuples of name of valve and the minute in which it was opened

        # If nothing happens from now until the end of the time, then the maximum pressure that can be released
        # is the result of the currently open valves
        max_released = sum(valves[name] * (time_limit - opened_at) for name, opened_at in open_valves)

        for next_room, distance in shortest_paths[location].items():
            # If next_room does not have an open valve
            if not next_room in [valve[0] for valve in open_valves]:
                # If next_room can be reached and opened before the end of the time allowed
                if minute + distance <= time_limit:
                    # Open the valve at minute + distance - 1, because minute + distance is when you're ready to take a new action.
                    # You will have therefore opened the valve 1 before that, hence the "- 1".
                    max_released = max(max_released, simulate(
                                                         minute + distance,
                                                         next_room,
                                                         open_valves.union([(next_room, minute + distance - 1)])
                                                     )
                                      )

        return max_released

    return simulate()

def main():
    puzzle_input = util.read.as_lines()

    pressure = solve(puzzle_input)

    print("The most pressure that can be released in 30 minutes is " + str(pressure) + ".")

class AOC_Tests(unittest.TestCase):
    def test_ex1(self):
        return self.assertEqual(solve(["Valve AA has flow rate=0; tunnels lead to valves DD, II, BB",
                                       "Valve BB has flow rate=13; tunnels lead to valves CC, AA",
                                       "Valve CC has flow rate=2; tunnels lead to valves DD, BB",
                                       "Valve DD has flow rate=20; tunnels lead to valves CC, AA, EE",
                                       "Valve EE has flow rate=3; tunnels lead to valves FF, DD",
                                       "Valve FF has flow rate=0; tunnels lead to valves EE, GG",
                                       "Valve GG has flow rate=0; tunnels lead to valves FF, HH",
                                       "Valve HH has flow rate=22; tunnel leads to valve GG",
                                       "Valve II has flow rate=0; tunnels lead to valves AA, JJ",
                                       "Valve JJ has flow rate=21; tunnel leads to valve II"]), 1651)

run(main)
