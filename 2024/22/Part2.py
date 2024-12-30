#!/usr/bin/env python3

#Advent of Code
#2024 Day 22, Part 2
#Solution by James C. (https://github.com/JamesMCo)

import os, sys
sys.path.append(os.path.abspath("../.."))
import unittest, util.read
from util.tests import run

def solve(puzzle_input: list[int]) -> int:
    # Steps to evolve a secret number:
    # Multiply by 64, mix, and prune   => left shift 6,  XOR with original, AND with 16777215
    # Divide by 32, mix, and prune     => right shift 5, XOR with original, AND with 16777215
    # Multiply by 2048, mix, and prune => left shift 11, XOR with original, AND with 16777215
    def evolve(original: int) -> int:
        working = ((original << 6) ^ original) & 16777215
        working = ((working >> 5) ^ working) & 16777215
        return ((working << 11) ^ working) & 16777215

    def generate(n: int) -> list[int]:
        output: list[int] = [n]
        for _ in range(2000):
            output.append(evolve(output[-1]))
        return list(map(lambda x: x % 10, output))

    def find_deltas(l: list[int]) -> list[tuple[int, int, int, int]]:
        ds: list[tuple[int, int, int, int]] = []
        for i in range(0, len(l) - 4):
            # Scans the entire list such that we can extract 5 numbers at a time (for 4 deltas at a time)
            ds.append(tuple(l[j+1] - l[j] for j in range(i, i+4)))
        return ds

    monkeys: list[list[int]] = list(map(generate, puzzle_input))
    deltas: list[list[tuple[int, int, int, int]]] = list(map(find_deltas, monkeys))
    delta_sets: list[set[tuple[int, int, int, int]]] = list(map(set, deltas))

    def test_pattern(ds: tuple[int, int, int, int]) -> int:
        bananas: int = 0
        for monkey, monkey_deltas, monkey_delta_set in zip(monkeys, deltas, delta_sets):
            if ds in monkey_delta_set:
                bananas += monkey[monkey_deltas.index(ds) + 4]
        return bananas

    possible_patterns: set[tuple[int, int, int, int]] = set().union(*delta_sets)
    return max(map(test_pattern, possible_patterns))

def main() -> tuple[str, int]:
    puzzle_input = util.read.as_int_list("\n")

    return "The most bananas you can get is {}.", solve(puzzle_input)

class AOC_Tests(unittest.TestCase):
    def test_ex1(self):
        return self.assertEqual(solve([1, 2, 3, 2024]), 23)

if __name__ == "__main__":
    run(main)
