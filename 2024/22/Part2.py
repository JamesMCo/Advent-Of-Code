#!/usr/bin/env python3

#Advent of Code
#2024 Day 22, Part 2
#Solution by James C. (https://github.com/JamesMCo)

import os, sys
sys.path.append(os.path.abspath("../.."))
import unittest, util.read
from util.tests import run

from collections import defaultdict

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

    deltas: defaultdict[tuple[int, int, int, int], int] = defaultdict(int)

    def find_deltas_to_bananas(n: int) -> None:
        l: list[int] = generate(n)

        seen: set[tuple[int, int, int, int]] = set()
        for i in range(0, len(l) - 4):
            # Scans the entire list such that we can extract 5 numbers at a time (for 4 deltas at a time)
            if (delta_pattern := tuple(l[j+1] - l[j] for j in range(i, i+4))) not in seen:
                # Save the number of bananas that would be awarded if using this pattern
                # (so if deltas is in seen, we've already seen the pattern before and wouldn't reach this stage)
                deltas[delta_pattern] += l[i + 4]
                seen.add(delta_pattern)

    for monkey in puzzle_input:
        find_deltas_to_bananas(monkey)
    return max(deltas.values())

def main() -> tuple[str, int]:
    puzzle_input = util.read.as_int_list("\n")

    return "The most bananas you can get is {}.", solve(puzzle_input)

class AOC_Tests(unittest.TestCase):
    def test_ex1(self):
        return self.assertEqual(solve([1, 2, 3, 2024]), 23)

if __name__ == "__main__":
    run(main)
