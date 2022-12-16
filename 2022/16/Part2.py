#!/usr/bin/env python3

#Advent of Code
#2022 Day 16, Part 2
#Solution by James C. (https://github.com/JamesMCo)

import os, sys
sys.path.append(os.path.abspath("../.."))
import unittest, util.read
from util.tests import run

from functools import cache
import networkx as nx
import re

def solve(puzzle_input):
    time_limit = 26

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

    results = {}

    @cache
    def simulate(minute=1, location="AA", open_valves=frozenset()):
        # Minute      := int from 1 to 26
        # Location    := string name of valve in current room
        # Open valves := set of tuples of name of valve and the minute in which it was opened

        # If nothing happens from now until the end of the time, then the maximum pressure that can be released
        # is the result of the currently open valves
        max_released = sum(valves[name] * (time_limit - opened_at) for name, opened_at in open_valves)
        
        # Save the most pressure able to be released (that has been found so far) with only these open valves
        lookup_key = frozenset([name for name, opened_at in open_valves])
        if lookup_key not in results:
            results[lookup_key] = max_released
        elif results[lookup_key] < max_released:
                results[lookup_key] = max_released

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

    # Part 2 specific changes derived from this reddit comment by /u/RewrittenCodeA
    # https://www.reddit.com/r/adventofcode/comments/zn6k1l/comment/j0h282i/

    # For a long time, there was a bug on line 60 where I was checking for strictly less than, rather than less than or equal.
    # Since taking a turn just after the time cutoff would mean you opened a valve just before the time cutoff, it would
    # release some pressure. As a result, this needed to be a less than or equal check.
    #
    # This bug existed (but has been fixed) in my part 1 solution, but didn't affect the final result.
    # Typical.

    # Generate all paths, saved in results list
    simulate()
    # Results is now a list of tuples [(pressure_released, set(open_valves))]
    results_list = [(pressure_released, open_valves) for open_valves, pressure_released in results.items()]
    results_list.sort(key=lambda x: x[0], reverse=True)

    max_overall = 0
    for i, path1 in enumerate(results_list[:-1]):
        for path2 in results_list[i+1:]:
            if path1[1].isdisjoint(path2[1]):
                if path1[0] + path2[0] > max_overall:
                    max_overall = path1[0] + path2[0]
                else:
                    break

    return max_overall

def main():
    puzzle_input = util.read.as_lines()

    pressure = solve(puzzle_input)

    print("The most pressure that can be released with the help of an elephant in 26 minutes is " + str(pressure) + ".")

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
                                       "Valve JJ has flow rate=21; tunnel leads to valve II"]), 1707)

run(main)
