#!/usr/bin/env python3

#Advent of Code
#2025 Day 7, Part 1
#Solution by James C. (https://github.com/JamesMCo)

import os, sys
sys.path.append(os.path.abspath("../.."))
import unittest, util.read
from util.tests import run

def solve(puzzle_input: list[str]) -> int:
    beams: set[int] = {puzzle_input[0].find("S")}
    splits: int = 0
    for row in puzzle_input[1:]:
        new_beams: set[int] = set()
        for beam in beams:
            if row[beam] == "^":
                new_beams.add(beam - 1)
                new_beams.add(beam + 1)
                splits += 1
            else:
                new_beams.add(beam)
        beams = new_beams
    return splits

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
                                       "..............."]), 21)

if __name__ == "__main__":
    run(main)
