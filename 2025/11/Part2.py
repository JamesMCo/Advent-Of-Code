#!/usr/bin/env python3

#Advent of Code
#2025 Day 11, Part 2
#Solution by James C. (https://github.com/JamesMCo)

import os, sys
sys.path.append(os.path.abspath("../.."))
import unittest, util.read
from util.tests import run

def solve(puzzle_input: list[str]) -> int:
    nodes: dict[str, set[str]] = {line.split()[0][:-1]: set(line.split()[1:]) for line in puzzle_input}

    def find_outward_paths(from_node: str, target_node: str, avoiding: list[str], previous_path: list[str], cache: dict[str, int]) -> int:
        if from_node not in cache:
            if from_node == target_node:
                cache[from_node] = 1
            else:
                outward_paths: int = 0
                for next_node in nodes[from_node]:
                    if next_node != from_node and next_node not in previous_path and next_node not in avoiding:
                        outward_paths += find_outward_paths(next_node, target_node, avoiding, previous_path + [from_node], cache)
                cache[from_node] = outward_paths
        return cache[from_node]

    svr_to_dac: int = find_outward_paths("svr", "dac", ["fft", "out"], [], {})
    dac_to_fft: int = find_outward_paths("dac", "fft", ["svr", "out"], [], {})
    fft_to_out: int = find_outward_paths("fft", "out", ["svr", "dac"], [], {})

    svr_to_fft: int = find_outward_paths("svr", "fft", ["dac", "out"], [], {})
    fft_to_dac: int = find_outward_paths("fft", "dac", ["svr", "out"], [], {})
    dac_to_out: int = find_outward_paths("dac", "out", ["svr", "dac"], [], {})

    return (svr_to_dac * dac_to_fft * fft_to_out) + (svr_to_fft * fft_to_dac * dac_to_out)

def main() -> tuple[str, int]:
    puzzle_input = util.read.as_lines()

    return "The number of paths leading from svr to out via dac and fft is {}.", solve(puzzle_input)

class AOC_Tests(unittest.TestCase):
    def test_ex1(self):
        return self.assertEqual(solve(["svr: aaa bbb",
                                       "aaa: fft",
                                       "fft: ccc",
                                       "bbb: tty",
                                       "tty: ccc",
                                       "ccc: ddd eee",
                                       "ddd: hub",
                                       "hub: fff",
                                       "eee: dac",
                                       "dac: fff",
                                       "fff: ggg hhh",
                                       "ggg: out",
                                       "hhh: out"]), 2)

if __name__ == "__main__":
    run(main)
