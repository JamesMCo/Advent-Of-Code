#!/usr/bin/env python3

#Advent of Code
#2024 Day 9, Part 1
#Solution by James C. (https://github.com/JamesMCo)

import os, sys
sys.path.append(os.path.abspath("../.."))
import unittest, util.read
from util.tests import run

from typing import Generator

def solve(puzzle_input: list[int]) -> int:
    total_blocks: int = sum(puzzle_input[::2])

    def get_blocks_from_end() -> Generator[int]:
        curr_id: int = len(puzzle_input[::2]) - 1
        for digit in puzzle_input[::-2]:
            for _ in range(digit):
                yield curr_id
            curr_id -= 1

    def get_compacted_blocks() -> Generator[int]:
        backwards_blocks: Generator[int] = get_blocks_from_end()
        yielded_blocks: int = 0

        is_file: bool = True
        curr_id: int = 0
        for digit in puzzle_input:
            if is_file:
                for _ in range(digit):
                    yield curr_id
                    yielded_blocks += 1
                    if yielded_blocks == total_blocks:
                        return
                curr_id += 1
            else:
                for _ in range(digit):
                    yield next(backwards_blocks)
                    yielded_blocks += 1
                    if yielded_blocks == total_blocks:
                        return
            is_file = not is_file

    return sum(position * file_id for position, file_id in enumerate(get_compacted_blocks()))

def main() -> tuple[str, int]:
    puzzle_input = [int(n) for n in util.read.as_string()]

    return "The filesystem checksum is {}.", solve(puzzle_input)

class AOC_Tests(unittest.TestCase):
    def test_ex1(self):
        return self.assertEqual(solve([int(n) for n in "12345"]), 60)

    def test_ex2(self):
        return self.assertEqual(solve([int(n) for n in "2333133121414131402"]), 1928)

run(main)
