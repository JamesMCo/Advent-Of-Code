#!/usr/bin/env python3

#Advent of Code
#2024 Day 20, Part 1
#Solution by James C. (https://github.com/JamesMCo)

import os, sys
sys.path.append(os.path.abspath("../.."))
import unittest, util.read
from util.tests import run

from collections import deque
import networkx as nx
from typing import TypeAlias

cheat_type: TypeAlias = None | tuple[tuple[int, int], None] | tuple[tuple[int, int], tuple[int, int]]

def solve(puzzle_input: list[str], saved_threshold: int = 100, exact_threshold: bool = False) -> int:
    width: int = len(puzzle_input[0])
    height: int = len(puzzle_input)

    start: tuple[int, int] = (-1, -1)
    end: tuple[int, int] = (-1, -1)

    graph: nx.Graph = nx.Graph()
    walls: set[tuple[int, int]] = set()
    for y, row in enumerate(puzzle_input):
        for x, col in enumerate(row):
            if col == "#":
                walls.add((x, y))
            else:
                if col == "S":
                    start = (x, y)
                elif col == "E":
                    end = (x, y)
                for neighbour_loc in [(x, y - 1), (x - 1, y), (x, y + 1), (x + 1, y)]:
                    if puzzle_input[neighbour_loc[1]][neighbour_loc[0]] != "#":
                        graph.add_edge((x, y), neighbour_loc)

    shortest_paths: dict[tuple[int, int], int] = {source: length for source, length in nx.single_target_shortest_path_length(graph, end)}

    def count_cheats(no_cheat_min: int) -> dict[int, int]:
        queue: deque[tuple[tuple[int, int], set[tuple[int, int]], cheat_type]] = deque([(start, set(), None)])
        queued: set[tuple[tuple[int, int], cheat_type]] = {(start, None)}
        output: dict[int, set[cheat_type]] = {}
        while queue:
            current_loc: tuple[int, int]
            current_path: set[tuple[int, int]]
            current_cheat: cheat_type
            current_loc, current_path, current_cheat = queue.popleft()

            if current_loc[0] < 0 or current_loc[0] >= width or current_loc[1] < 0 or current_loc[1] >= height:
                # Can't move out of bounds
                continue
            elif len(current_path) > no_cheat_min - saved_threshold:
                # The current path already does not save enough length
                continue
            else:
                for neighbour in [
                    (current_loc[0], current_loc[1] - 1),
                    (current_loc[0] - 1, current_loc[1]),
                    (current_loc[0], current_loc[1] + 1),
                    (current_loc[0] + 1, current_loc[1])
                ]:
                    if current_cheat is None:
                        # We can cheat, or we can choose not to cheat
                        if neighbour in walls:
                            # Choosing to cheat
                            if (neighbour, (current_loc, None)) not in queued:
                                queue.append((neighbour, current_path | {current_loc}, (current_loc, None)))
                                queued.add((neighbour, (current_loc, None)))
                        else:
                            # Choosing not to cheat
                            if (neighbour, None) not in queued:
                                queue.append((neighbour, current_path | {current_loc}, None))
                                queued.add((neighbour, None))
                    elif current_cheat[1] is None:
                        # Must consider this move as the end of a cheat, and must end up not in a wall
                        if neighbour not in walls:
                            if (neighbour, (current_cheat[0], neighbour)) not in queued:
                                queue.append((neighbour, current_path | {current_loc}, (current_cheat[0], neighbour)))
                                queued.add((neighbour, (current_cheat[0], neighbour)))
                    else:
                        # No more cheating allowed
                        # Anything from here is therefore equivalent to a normal shortest path
                        saved_length: int = no_cheat_min - len(current_path) - shortest_paths[current_loc]
                        if saved_length not in output:
                            output[saved_length] = {current_cheat}
                        else:
                            output[saved_length].add(current_cheat)

        return {saved_amount: len(cheats) for saved_amount, cheats in output.items()}

    return sum(count for saved_amount, count in count_cheats(shortest_paths[start]).items() if (saved_amount == saved_threshold if exact_threshold else saved_amount >= saved_threshold))

def main() -> tuple[str, int]:
    puzzle_input = util.read.as_lines()

    return "The number of cheats that would save at least 100 picoseconds is {}.", solve(puzzle_input)

class AOC_Tests(unittest.TestCase):
    def test_ex1(self):
        return self.assertEqual(solve(["###############",
                                       "#...#...#.....#",
                                       "#.#.#.#.#.###.#",
                                       "#S#...#.#.#...#",
                                       "#######.#.#.###",
                                       "#######.#.#...#",
                                       "#######.#.###.#",
                                       "###..E#...#...#",
                                       "###.#######.###",
                                       "#...###...#...#",
                                       "#.#####.#.###.#",
                                       "#.#...#.#.#...#",
                                       "#.#.#.#.#.#.###",
                                       "#...#...#...###",
                                       "###############"], 2, True), 14)

    def test_ex2(self):
        return self.assertEqual(solve(["###############",
                                       "#...#...#.....#",
                                       "#.#.#.#.#.###.#",
                                       "#S#...#.#.#...#",
                                       "#######.#.#.###",
                                       "#######.#.#...#",
                                       "#######.#.###.#",
                                       "###..E#...#...#",
                                       "###.#######.###",
                                       "#...###...#...#",
                                       "#.#####.#.###.#",
                                       "#.#...#.#.#...#",
                                       "#.#.#.#.#.#.###",
                                       "#...#...#...###",
                                       "###############"], 4, True), 14)

    def test_ex3(self):
        return self.assertEqual(solve(["###############",
                                       "#...#...#.....#",
                                       "#.#.#.#.#.###.#",
                                       "#S#...#.#.#...#",
                                       "#######.#.#.###",
                                       "#######.#.#...#",
                                       "#######.#.###.#",
                                       "###..E#...#...#",
                                       "###.#######.###",
                                       "#...###...#...#",
                                       "#.#####.#.###.#",
                                       "#.#...#.#.#...#",
                                       "#.#.#.#.#.#.###",
                                       "#...#...#...###",
                                       "###############"], 6, True), 2)

    def test_ex4(self):
        return self.assertEqual(solve(["###############",
                                       "#...#...#.....#",
                                       "#.#.#.#.#.###.#",
                                       "#S#...#.#.#...#",
                                       "#######.#.#.###",
                                       "#######.#.#...#",
                                       "#######.#.###.#",
                                       "###..E#...#...#",
                                       "###.#######.###",
                                       "#...###...#...#",
                                       "#.#####.#.###.#",
                                       "#.#...#.#.#...#",
                                       "#.#.#.#.#.#.###",
                                       "#...#...#...###",
                                       "###############"], 8, True), 4)

    def test_ex5(self):
        return self.assertEqual(solve(["###############",
                                       "#...#...#.....#",
                                       "#.#.#.#.#.###.#",
                                       "#S#...#.#.#...#",
                                       "#######.#.#.###",
                                       "#######.#.#...#",
                                       "#######.#.###.#",
                                       "###..E#...#...#",
                                       "###.#######.###",
                                       "#...###...#...#",
                                       "#.#####.#.###.#",
                                       "#.#...#.#.#...#",
                                       "#.#.#.#.#.#.###",
                                       "#...#...#...###",
                                       "###############"], 10, True), 2)

    def test_ex6(self):
        return self.assertEqual(solve(["###############",
                                       "#...#...#.....#",
                                       "#.#.#.#.#.###.#",
                                       "#S#...#.#.#...#",
                                       "#######.#.#.###",
                                       "#######.#.#...#",
                                       "#######.#.###.#",
                                       "###..E#...#...#",
                                       "###.#######.###",
                                       "#...###...#...#",
                                       "#.#####.#.###.#",
                                       "#.#...#.#.#...#",
                                       "#.#.#.#.#.#.###",
                                       "#...#...#...###",
                                       "###############"], 12, True), 3)

    def test_ex7(self):
        return self.assertEqual(solve(["###############",
                                       "#...#...#.....#",
                                       "#.#.#.#.#.###.#",
                                       "#S#...#.#.#...#",
                                       "#######.#.#.###",
                                       "#######.#.#...#",
                                       "#######.#.###.#",
                                       "###..E#...#...#",
                                       "###.#######.###",
                                       "#...###...#...#",
                                       "#.#####.#.###.#",
                                       "#.#...#.#.#...#",
                                       "#.#.#.#.#.#.###",
                                       "#...#...#...###",
                                       "###############"], 20, True), 1)

    def test_ex8(self):
        return self.assertEqual(solve(["###############",
                                       "#...#...#.....#",
                                       "#.#.#.#.#.###.#",
                                       "#S#...#.#.#...#",
                                       "#######.#.#.###",
                                       "#######.#.#...#",
                                       "#######.#.###.#",
                                       "###..E#...#...#",
                                       "###.#######.###",
                                       "#...###...#...#",
                                       "#.#####.#.###.#",
                                       "#.#...#.#.#...#",
                                       "#.#.#.#.#.#.###",
                                       "#...#...#...###",
                                       "###############"], 36, True), 1)

    def test_ex9(self):
        return self.assertEqual(solve(["###############",
                                       "#...#...#.....#",
                                       "#.#.#.#.#.###.#",
                                       "#S#...#.#.#...#",
                                       "#######.#.#.###",
                                       "#######.#.#...#",
                                       "#######.#.###.#",
                                       "###..E#...#...#",
                                       "###.#######.###",
                                       "#...###...#...#",
                                       "#.#####.#.###.#",
                                       "#.#...#.#.#...#",
                                       "#.#.#.#.#.#.###",
                                       "#...#...#...###",
                                       "###############"], 38, True), 1)

    def test_ex10(self):
        return self.assertEqual(solve(["###############",
                                       "#...#...#.....#",
                                       "#.#.#.#.#.###.#",
                                       "#S#...#.#.#...#",
                                       "#######.#.#.###",
                                       "#######.#.#...#",
                                       "#######.#.###.#",
                                       "###..E#...#...#",
                                       "###.#######.###",
                                       "#...###...#...#",
                                       "#.#####.#.###.#",
                                       "#.#...#.#.#...#",
                                       "#.#.#.#.#.#.###",
                                       "#...#...#...###",
                                       "###############"], 40, True), 1)

    def test_ex11(self):
        return self.assertEqual(solve(["###############",
                                       "#...#...#.....#",
                                       "#.#.#.#.#.###.#",
                                       "#S#...#.#.#...#",
                                       "#######.#.#.###",
                                       "#######.#.#...#",
                                       "#######.#.###.#",
                                       "###..E#...#...#",
                                       "###.#######.###",
                                       "#...###...#...#",
                                       "#.#####.#.###.#",
                                       "#.#...#.#.#...#",
                                       "#.#.#.#.#.#.###",
                                       "#...#...#...###",
                                       "###############"], 64, True), 1)

run(main)
