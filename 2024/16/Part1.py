#!/usr/bin/env python3

#Advent of Code
#2024 Day 16, Part 1
#Solution by James C. (https://github.com/JamesMCo)

import os, sys
sys.path.append(os.path.abspath("../.."))
import unittest, util.read
from util.tests import run

import networkx as nx

def solve(puzzle_input: list[str]) -> int:
    width: int = len(puzzle_input[0])
    height: int = len(puzzle_input)

    start: tuple[int, int] = (-1, -1)
    end: tuple[int, int] = (-1, -1)

    graph = nx.DiGraph()
    for y, row in enumerate(puzzle_input):
        for x, col in enumerate(row):
            if col == "#":
                # Can't be inside a wall
                continue
            elif col == "S":
                start = (x, y)
            elif col == "E":
                end = (x, y)

            graph.add_weighted_edges_from([
                ((x, y, "N"), (x, y, "E"), 1000),
                ((x, y, "E"), (x, y, "N"), 1000),

                ((x, y, "E"), (x, y, "S"), 1000),
                ((x, y, "S"), (x, y, "E"), 1000),

                ((x, y, "S"), (x, y, "W"), 1000),
                ((x, y, "W"), (x, y, "S"), 1000),

                ((x, y, "W"), (x, y, "N"), 1000),
                ((x, y, "N"), (x, y, "W"), 1000),
            ])

            for neighbour_x, neighbour_y, source_dir, dest_dir in [
                (x, y - 1, "N", "S"),
                (x + 1, y, "E", "W"),
                (x, y + 1, "S", "N"),
                (x - 1, y, "W", "E")
            ]:
                if neighbour_x < 0 or neighbour_x >= width:
                    # Out of bounds horizontally
                    continue
                elif neighbour_y < 0 or neighbour_y >= height:
                    # Out of bounds vertically
                    continue
                elif puzzle_input[neighbour_y][neighbour_x] == "#":
                    # Can't walk in to a wall
                    continue
                else:
                    graph.add_weighted_edges_from([
                        ((x, y, source_dir), (neighbour_x, neighbour_y, source_dir), 1),
                        ((neighbour_x, neighbour_y, dest_dir), (x, y, dest_dir), 1)
                    ])

    shortest_path_lengths: dict[tuple[int, int, str], int] = nx.single_source_dijkstra_path_length(graph, (start[0], start[1], "E"))
    return min(shortest_path_lengths[(end[0], end[1], d)] for d in "NESW")

def main() -> tuple[str, int]:
    puzzle_input = util.read.as_lines()

    return "The lowest score a Reindeer could possibly get is {}.", solve(puzzle_input)

class AOC_Tests(unittest.TestCase):
    def test_ex1(self):
        return self.assertEqual(solve(["###############",
                                       "#.......#....E#",
                                       "#.#.###.#.###.#",
                                       "#.....#.#...#.#",
                                       "#.###.#####.#.#",
                                       "#.#.#.......#.#",
                                       "#.#.#####.###.#",
                                       "#...........#.#",
                                       "###.#.#####.#.#",
                                       "#...#.....#.#.#",
                                       "#.#.#.###.#.#.#",
                                       "#.....#...#.#.#",
                                       "#.###.#.#.#.#.#",
                                       "#S..#.....#...#",
                                       "###############"]), 7036)

    def test_ex2(self):
        return self.assertEqual(solve(["#################",
                                       "#...#...#...#..E#",
                                       "#.#.#.#.#.#.#.#.#",
                                       "#.#.#.#...#...#.#",
                                       "#.#.#.#.###.#.#.#",
                                       "#...#.#.#.....#.#",
                                       "#.#.#.#.#.#####.#",
                                       "#.#...#.#.#.....#",
                                       "#.#.#####.#.###.#",
                                       "#.#.#.......#...#",
                                       "#.#.###.#####.###",
                                       "#.#.#...#.....#.#",
                                       "#.#.#.#####.###.#",
                                       "#.#.#.........#.#",
                                       "#.#.#.#########.#",
                                       "#S#.............#",
                                       "#################"]), 11048)

if __name__ == "__main__":
    run(main)
