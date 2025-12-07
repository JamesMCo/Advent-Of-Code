#!/usr/bin/env python3

#Advent of Code
#2025 Day 7, Part 2
#Solution by James C. (https://github.com/JamesMCo)

import os, sys
sys.path.append(os.path.abspath("../.."))
import unittest, util.read
from util.tests import run

from collections import defaultdict

def solve(puzzle_input: list[str]) -> int:
    beams: defaultdict[int, int] = defaultdict(int)
    beams[puzzle_input[0].find("S")] = 1
    for row in puzzle_input[1:]:
        new_beams: defaultdict[int, int] = defaultdict(int)
        for beam in beams:
            if row[beam] == "^":
                new_beams[beam - 1] += beams[beam]
                new_beams[beam + 1] += beams[beam]
            else:
                new_beams[beam] += beams[beam]
        beams = new_beams
    return sum(beams.values())

def main() -> tuple[str, int]:
    puzzle_input = util.read.as_lines()

    return "The number of times that the beam will split is {}.", solve(puzzle_input)

class AOC_Tests(unittest.TestCase):
    def test_ex1(self):
        return self.assertEqual(solve([".......S.......",
                                       "...............",
                                       ".......^.......",
                                       "...............",
                                       "......^.^......",
                                       "...............",
                                       ".....^.^.^.....",
                                       "...............",
                                       "....^.^...^....",
                                       "...............",
                                       "...^.^...^.^...",
                                       "...............",
                                       "..^...^.....^..",
                                       "...............",
                                       ".^.^.^.^.^...^.",
                                       "..............."]), 40)

if __name__ == "__main__":
    run(main)
