#!/usr/bin/env python3

#Advent of Code
#2023 Day 23, Part 2
#Solution by James C. (https://github.com/JamesMCo)

import os, sys
sys.path.append(os.path.abspath("../.."))
import unittest, util.read
from util.tests import run

from collections import deque

def solve(puzzle_input: list[str]) -> int:
    width = len(puzzle_input[0])
    height = len(puzzle_input)

    start = (puzzle_input[0].index("."), 0, )
    target = (puzzle_input[-1].index("."), height - 1)

    def neighbours(x: int, y: int) -> set[tuple[int, int]]:
        output: set[tuple[int, int]] = set()
        for dx, dy in ((0, -1), (1, 0), (0, 1), (-1, 0)):
            if 0 <= x + dx < width and 0 <= y + dy < height and puzzle_input[y + dy][x + dx] != "#":
                output.add((x + dx, y + dy))
        return output

    def build_graph() -> dict[tuple[int, int], dict[tuple[int, int], int]]:
        output = {}
        # Find all junctions (& start/target)
        for y, row in enumerate(puzzle_input):
            for x, col in enumerate(row):
                if col != "#":
                    if len(neighbours(x, y)) > 2 or (x, y) in (start, target):
                        output[(x, y)] = {}
        # Find paths between junctions
        for junction in output:
            queue: deque[tuple[tuple[int, int], set[tuple[int, int]]]] = deque()
            junction_neighbours = neighbours(*junction)
            if len(junction_neighbours) != len(output[junction]):
                # If not already found all neighbouring paths
                queue.extend([(neighbour, {junction}) for neighbour in junction_neighbours])
                while queue:
                    from_coord, seen = queue.popleft()
                    while True:
                        next_cells = neighbours(*from_coord) - seen
                        if len(next_cells) == 0:
                            # If 0 next cells, then we're at a dead end. We don't need to consider this path.
                            break
                        if len(next_cells) == 1:
                            # If only one option, skip immediately to consider it
                            seen |= {from_coord}
                            (from_coord,) = next_cells
                        elif len(next_cells) >= 2 and from_coord != junction:
                            # Found a junction that isn't the one we're originating from
                            output[junction][from_coord] = output[from_coord][junction] = len(seen)
                            break
        return output

    graph = build_graph()
    queue: deque[tuple[tuple[int, int], set[tuple[int, int]], int]] = deque()
    queue.append((start, set(), 0))
    longest_length = 0

    while queue:
        from_coord, seen, length = queue.popleft()

        if from_coord == target:
            longest_length = max(longest_length, length)
            break

        next_cells = list(graph[from_coord])
        if target in next_cells:
            # If can go to the target, *must* go to the target (otherwise block it off)
            longest_length = max(longest_length, length + graph[from_coord][target])
        else:
            queue.extend((next_cell, seen | {from_coord}, length + graph[from_coord][next_cell]) for next_cell in next_cells if next_cell not in seen)

    return longest_length

def main() -> tuple[str, int]:
    puzzle_input = util.read.as_lines()

    return "The longest hike is {} steps long.", solve(puzzle_input)

class AOC_Tests(unittest.TestCase):
    def test_ex1(self):
        return self.assertEqual(solve(["#.#####################",
                                       "#.......#########...###",
                                       "#######.#########.#.###",
                                       "###.....#.>.>.###.#.###",
                                       "###v#####.#v#.###.#.###",
                                       "###.>...#.#.#.....#...#",
                                       "###v###.#.#.#########.#",
                                       "###...#.#.#.......#...#",
                                       "#####.#.#.#######.#.###",
                                       "#.....#.#.#.......#...#",
                                       "#.#####.#.#.#########v#",
                                       "#.#...#...#...###...>.#",
                                       "#.#.#v#######v###.###v#",
                                       "#...#.>.#...>.>.#.###.#",
                                       "#####v#.#.###v#.#.###.#",
                                       "#.....#...#...#.#.#...#",
                                       "#.#########.###.#.#.###",
                                       "#...###...#...#...#.###",
                                       "###.###.#.###v#####v###",
                                       "#...#...#.#.>.>.#.>.###",
                                       "#.###.###.#.###.#.#v###",
                                       "#.....###...###...#...#",
                                       "#####################.#"]), 154)

if __name__ == "__main__":
    run(main)
