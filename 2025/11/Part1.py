#!/usr/bin/env python3

#Advent of Code
#2025 Day 11, Part 1
#Solution by James C. (https://github.com/JamesMCo)

import os, sys
sys.path.append(os.path.abspath("../.."))
import unittest, util.read
from util.tests import run

def solve(puzzle_input: list[str]) -> int:
    nodes: dict[str, set[str]] = {line.split()[0][:-1]: set(line.split()[1:]) for line in puzzle_input}

    def find_outward_paths(from_node: str, target_node: str, previous_path: list[str], cache: dict[str, int]) -> int:
        if from_node not in cache:
            if from_node == target_node:
                cache[from_node] = 1
            else:
                outward_paths: int = 0
                for next_node in nodes[from_node]:
                    if next_node != from_node and next_node not in previous_path:
                        outward_paths += find_outward_paths(next_node, target_node, previous_path + [from_node], cache)
                cache[from_node] = outward_paths
        return cache[from_node]

    return find_outward_paths("you", "out", [], {})

def main() -> tuple[str, int]:
    puzzle_input = util.read.as_lines()

    return "The number of paths leading from you to out is {}.", solve(puzzle_input)

class AOC_Tests(unittest.TestCase):
    def test_ex1(self):
        return self.assertEqual(solve(["aaa: you hhh",
                                       "you: bbb ccc",
                                       "bbb: ddd eee",
                                       "ccc: ddd eee fff",
                                       "ddd: ggg",
                                       "eee: out",
                                       "fff: out",
                                       "ggg: out",
                                       "hhh: ccc fff iii",
                                       "iii: out"]), 5)

if __name__ == "__main__":
    run(main)
