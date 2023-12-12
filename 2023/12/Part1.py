#!/usr/bin/env python3

#Advent of Code
#2023 Day 12, Part 1
#Solution by James C. (https://github.com/JamesMCo)

import os, sys
sys.path.append(os.path.abspath("../.."))
import unittest, util.read
from util.tests import run

from itertools import product
import re
import typing as t

def solve(puzzle_input: list[str]) -> int:
    def get_fills(slots: int, total_springs: int, existing_springs: int) -> t.Iterable[t.Iterable[str]]:
        for arrangement in product(".#", repeat=slots):
            if existing_springs + arrangement.count("#") == total_springs:
                yield iter(arrangement)

    def is_valid(springs: t.Iterable[str], fill: t.Iterable[str], groups: t.Iterable[int]) -> bool:
        filled_springs = "".join(next(fill) if c == "?" else c for c in springs)
        contiguous_groups = re.findall(r"#+", filled_springs)
        return all(a == b for a, b in zip(map(len, contiguous_groups), groups))

    def count_arrangements(line: str) -> int:
        springs = line.split()[0]
        groups = list(map(int, line.split()[1].split(",")))

        return sum(1 for fill in get_fills(springs.count("?"), sum(groups), springs.count("#")) if is_valid(springs, fill, groups))

    return sum(map(count_arrangements, puzzle_input))

def main() -> tuple[str, int]:
    puzzle_input = util.read.as_lines()

    return "The sum of the arrangements for all lines is {}.", solve(puzzle_input)

class AOC_Tests(unittest.TestCase):
    def test_ex1(self):
        return self.assertEqual(solve(["???.### 1,1,3",
                                       ".??..??...?##. 1,1,3",
                                       "?#?#?#?#?#?#?#? 1,3,1,6",
                                       "????.#...#... 4,1,1",
                                       "????.######..#####. 1,6,5",
                                       "?###???????? 3,2,1"]), 21)

run(main)
