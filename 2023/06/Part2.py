#!/usr/bin/env python3

#Advent of Code
#2023 Day 6, Part 2
#Solution by James C. (https://github.com/JamesMCo)

import os, sys
sys.path.append(os.path.abspath("../.."))
import unittest, util.read
from util.tests import run

import re

def solve(puzzle_input: list[str]) -> int:
    record_time     = int("".join(re.findall(r"\d+", puzzle_input[0])))
    record_distance = int("".join(re.findall(r"\d+", puzzle_input[1])))

    shortest_beating_time = 0
    for t in range(record_time):
        if t * (record_time - t) > record_distance:
            shortest_beating_time = t
            break

    for t in range(record_time - 1, -1, -1):
        if t * (record_time - t) > record_distance:
            return t - shortest_beating_time + 1


def main() -> tuple[str, int]:
    puzzle_input = util.read.as_lines()

    return "The number of ways you can beat the record is {}.", solve(puzzle_input)

class AOC_Tests(unittest.TestCase):
    def test_ex1(self):
        return self.assertEqual(solve(["Time:      7  15   30",
                                       "Distance:  9  40  200"]), 71503)

run(main)
