#!/usr/bin/env python3

#Advent of Code
#2023 Day 6, Part 2
#Solution by James C. (https://github.com/JamesMCo)

import os, sys
sys.path.append(os.path.abspath("../.."))
import unittest, util.read
from util.tests import run

from itertools import chain
from math import sqrt
import re
import typing as t

def solve(puzzle_input: list[str]) -> int:
    def roots_of_quadratic(a: float, b: float, c: float) -> list[float]:
        roots: list[float] = []

        for op in [lambda x, y: x + y, lambda x, y: x - y]:
            try:
                roots.append(op(-b, sqrt(b**2 - (4*a*c))) / (2*a))
            except (ZeroDivisionError, ValueError) as e:
                pass

        return sorted(roots)

    def count_record_breaking_strategies(record_time: int, record_distance: int) -> int:
        # t * (record_time - t) > record_distance
        # record_time * t - t * t > record_distance
        # t^2 - record_time * t + record_distance > 0

        def root_to_candidates(n: float) -> t.Iterable[int]:
            # The root is likely not an integer, and depending on whether
            # it's the upper or lower bound, the actual integer value
            # we're looking for might be +- 1 from the floor of the root.

            return filter(
                lambda time: time * (record_time - time) > record_distance,
                (int(n) + dn for dn in range(-1, 2))
            )

        candidates: list[int] = list(chain.from_iterable(map(
            root_to_candidates,
            roots_of_quadratic(1, -record_time, record_distance)
        )))
        return candidates[-1] - candidates[0] + 1

    return count_record_breaking_strategies(
        int("".join(re.findall(r"\d+", puzzle_input[0]))),
        int("".join(re.findall(r"\d+", puzzle_input[1])))
    )

def main() -> tuple[str, int]:
    puzzle_input = util.read.as_lines()

    return "The number of ways you can beat the record is {}.", solve(puzzle_input)

class AOC_Tests(unittest.TestCase):
    def test_ex1(self):
        return self.assertEqual(solve(["Time:      7  15   30",
                                       "Distance:  9  40  200"]), 71503)

if __name__ == "__main__":
    run(main)
