#!/usr/bin/env python3

#Advent of Code
#2024 Day 21, Part 1
#Solution by James C. (https://github.com/JamesMCo)

import os, sys
sys.path.append(os.path.abspath("../.."))
import unittest, util.read
from util.tests import run

from itertools import pairwise
import networkx as nx
from typing import Callable

def solve(puzzle_input: list[str]) -> int:
    def build_graph(keypad_description: list[str]) -> nx.DiGraph:
        graph: nx.DiGraph = nx.DiGraph()

        width: int = len(keypad_description[0])
        height: int = len(keypad_description)
        for y, row in enumerate(keypad_description):
            for x, button in enumerate(row):
                if button == " ":
                    continue

                for from_direction, dx, dy in [("^", 0, -1), (">", 1, 0), ("v", 0, 1), ("<", -1, 0)]:
                    # Add edges to/from generic version of the button with no direction (for start and end pathfinding)
                    # When going to a generic version, use "A" as the direction to press the button
                    graph.add_edge(f"{button}{from_direction}", button, weight=10000, direction="A")
                    graph.add_edge(button, f"{button}{from_direction}", weight=10000, direction="")

                    # Add edges to other rotations of the same button
                    # (with a high weight to discourage rotating unnecessarily)
                    #
                    # Some research on the subreddit lead to the realisation that costs to turn should be based on
                    # the difficulty/length of key presses to press the buttons
                    # Left is hardest to press (furthest from A), then Down, then Up and Right
                    if from_direction != "<":
                        graph.add_edge(f"{button}{from_direction}", f"{button}<", weight=8000, direction="")
                    if from_direction != "v":
                        graph.add_edge(f"{button}{from_direction}", f"{button}v", weight=6000, direction="")
                    if from_direction != "^":
                        graph.add_edge(f"{button}{from_direction}", f"{button}^", weight=4000, direction="")
                    if from_direction != ">":
                        graph.add_edge(f"{button}{from_direction}", f"{button}>", weight=2000, direction="")

                    # Since we're facing a direction, we can only go in that direction

                    # Make sure it's a valid button
                    if x + dx < 0 or x + dx >= width or y + dy < 0 or y + dy >= height:
                        continue
                    elif (next_button := keypad_description[y + dy][x + dx]) == " ":
                        continue

                    # Add an edge to next button
                    graph.add_edge(f"{button}{from_direction}", f"{next_button}{from_direction}", weight=1, direction=from_direction)

        return graph

    def generic_keypad(graph: nx.DiGraph) -> Callable[[str], str]:
        shortest_paths: dict[str, dict[str, list[str]]] = dict(nx.all_pairs_dijkstra_path(graph))
        def inner(code: str) -> str:
            output: str = ""
            for prev_button, next_button in pairwise("A" + code):
                shortest_path: list[str] = shortest_paths[prev_button][next_button]
                if len(shortest_path) == 1:
                    # We were already on the button, just press it
                    output += "A"
                else:
                    for edge_from, edge_to in pairwise(shortest_path):
                        output += graph[edge_from][edge_to]["direction"]
            return output
        return inner

    numeric_keypad: Callable[[str], str] = generic_keypad(build_graph(["789","456","123"," 0A"]))
    directional_keypad: Callable[[str], str] = generic_keypad(build_graph([" ^A","<v>"]))

    def complexity(code: str) -> int:
        intermediate_code: str = code
        for keypad_func in [numeric_keypad] + ([directional_keypad] * 2):
            intermediate_code = keypad_func(intermediate_code)
        return len(intermediate_code) * int(code[:-1])

    return sum(map(complexity, puzzle_input))

def main() -> tuple[str, int]:
    puzzle_input = util.read.as_lines()

    return "The sum of the complexities is {}.", solve(puzzle_input)

class AOC_Tests(unittest.TestCase):
    def test_ex1(self):
        return self.assertEqual(solve(["029A",
                                       "980A",
                                       "179A",
                                       "456A",
                                       "379A"]), 126384)

if __name__ == "__main__":
    run(main)
