#!/usr/bin/env python3

#Advent of Code
#2024 Day 20, Part 2
#Solution by James C. (https://github.com/JamesMCo)

import os, sys
sys.path.append(os.path.abspath("../.."))
import unittest, util.read
from util.tests import run

from collections import deque
import networkx as nx
from typing import TypeAlias
from util.two_d_world import manhattan_distance

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

    shortest_paths: dict[tuple[int, int], int] = nx.single_target_shortest_path_length(graph, end)

    def count_cheats(no_cheat_min: int) -> dict[int, int]:
        queue: deque[tuple[tuple[int, int], set[tuple[int, int]]]] = deque([(start, set())])
        queued: set[tuple[tuple[int, int], cheat_type]] = {(start, None)}
        output: dict[cheat_type, int] = {}
        while queue:
            current_loc: tuple[int, int]
            current_path: set[tuple[int, int]]
            current_loc, current_path = queue.popleft()

            if current_loc[0] < 0 or current_loc[0] >= width or current_loc[1] < 0 or current_loc[1] >= height:
                # Can't move out of bounds
                continue
            elif len(current_path) > no_cheat_min - saved_threshold:
                # The current path already does not save enough length
                continue
            else:
                # We can cheat, or we can choose not to cheat
                # Choosing to cheat
                # After some reading on the subreddit, I realised the period spent cheating can be
                # replaced by jumping straight to any other path coordinate that is within 20 moves
                for y in range(-20, 21):
                    for x in range(-20, 21):
                        if x == 0 and y == 0:
                            continue
                        elif current_loc[0] + x < 0 or current_loc[0] + x >= width or current_loc[1] + y < 0 or current_loc[1] + y >= height:
                            continue
                        elif (spaces_moved := abs(x) + abs(y)) > 20:
                            continue
                        elif (current_loc[0] + x, current_loc[1] + y) in walls:
                            continue

                        # No need to push this state on to the queue, because we can just find the normal shortest path from the end point now
                        new_cheat: cheat_type = (current_loc, (current_loc[0] + x, current_loc[1] + y))
                        if new_cheat not in output:
                            output[new_cheat] = len(current_path) + spaces_moved + shortest_paths[new_cheat[1]]
                            #        +1 for the current location ^              ^ -1 for doubly counting the cheat end location
                            # (i.e. they cancel out)
                        else:
                            output[new_cheat] = min(output[new_cheat], len(current_path) + abs(x) + abs(y) + shortest_paths[new_cheat[1]])
                # Choosing not to cheat
                for neighbour in [
                    (current_loc[0], current_loc[1] - 1),
                    (current_loc[0] - 1, current_loc[1]),
                    (current_loc[0], current_loc[1] + 1),
                    (current_loc[0] + 1, current_loc[1])
                ]:
                    if neighbour not in walls and (neighbour, None) not in queued:
                        queue.append((neighbour, current_path | {current_loc}))
                        queued.add((neighbour, None))

        saved_lengths: dict[int, int] = {}
        for cheat, length in output.items():
            saved_length: int = no_cheat_min - length
            if saved_length not in saved_lengths:
                saved_lengths[saved_length] = 1
            else:
                saved_lengths[saved_length] += 1
        return saved_lengths

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
                                       "###############"], 50, True), 32)

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
                                       "###############"], 52, True), 31)

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
                                       "###############"], 54, True), 29)

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
                                       "###############"], 56, True), 39)

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
                                       "###############"], 58, True), 25)

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
                                       "###############"], 60, True), 23)

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
                                       "###############"], 62, True), 20)

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
                                       "###############"], 64, True), 19)

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
                                       "###############"], 66, True), 12)

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
                                       "###############"], 68, True), 14)

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
                                       "###############"], 70, True), 12)

    def test_ex12(self):
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
                                       "###############"], 72, True), 22)

    def test_ex13(self):
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
                                       "###############"], 74, True), 4)

    def test_ex14(self):
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
                                       "###############"], 76, True), 3)

if __name__ == "__main__":
    run(main)
