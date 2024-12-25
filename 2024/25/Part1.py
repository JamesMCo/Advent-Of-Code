#!/usr/bin/env python3

#Advent of Code
#2024 Day 25, Part 1
#Solution by James C. (https://github.com/JamesMCo)

import os, sys
sys.path.append(os.path.abspath("../.."))
import unittest, util.read
from util.tests import run

def solve(puzzle_input: list[str]) -> int:
    locks: set[tuple[int, int, int, int, int]] = set()
    keys: set[tuple[int, int, int, int, int]] = set()

    rows: list[str] = []
    for line in puzzle_input + [""]: # Add extra empty line at the end to ensure the final key is parsed (it's a bit flaky, but hey. It's Christmas.)
        if not line:
            if rows[0] == "#" * 5:
                locks.add(tuple(col.count("#") - 1 for col in zip(*rows)))
            else:
                keys.add(tuple(col.count("#") - 1 for col in zip(*rows)))
            rows = []
        else:
            rows.append(line)

    return sum(1 for lock in locks for key in keys if all(lock_col + key_col < 6 for lock_col, key_col in zip(lock, key)))

def main() -> tuple[str, int]:
    puzzle_input = util.read.as_lines()

    return "The number of unique lock/key pairs that fit together is {}.", solve(puzzle_input)

class AOC_Tests(unittest.TestCase):
    def test_ex1(self):
        return self.assertEqual(solve(["#####",
                                       ".####",
                                       ".####",
                                       ".####",
                                       ".#.#.",
                                       ".#...",
                                       ".....",
                                       "",
                                       "#####",
                                       "##.##",
                                       ".#.##",
                                       "...##",
                                       "...#.",
                                       "...#.",
                                       ".....",
                                       "",
                                       ".....",
                                       "#....",
                                       "#....",
                                       "#...#",
                                       "#.#.#",
                                       "#.###",
                                       "#####",
                                       "",
                                       ".....",
                                       ".....",
                                       "#.#..",
                                       "###..",
                                       "###.#",
                                       "###.#",
                                       "#####",
                                       "",
                                       ".....",
                                       ".....",
                                       ".....",
                                       "#....",
                                       "#.#..",
                                       "#.#.#",
                                       "#####"]), 3)

run(main)
