#!/usr/bin/env python3

#Advent of Code
#2023 Day 18, Part 2
#Solution by James C. (https://github.com/JamesMCo)

import os, sys
sys.path.append(os.path.abspath("../.."))
import unittest, util.read
from util.tests import run

import re

def solve(puzzle_input: list[str]) -> int:
    instruction_pattern: re.Pattern = re.compile(r"([UDLR]) (\d+) \((#[0-9a-f]{6})\)")

    # I didn't know how to approach part 2 of this puzzle, and so read some
    # discussions between some friends where they mentioned both Pick's algorithm
    # and the Shoelace formula. I hadn't heard of either of these before today,
    # so thank you, Day 18, for a learning opportunity!
    #
    # Pick's theorem: https://en.wikipedia.org/wiki/Pick%27s_theorem
    # Shoelace formula: https://en.wikipedia.org/wiki/Shoelace_formula

    vertices: list[tuple[int, int]] = [(0, 0)]
    current_x, current_y = (0, 0)
    perimeter_length = 1

    for line in puzzle_input:
        _, _, colour = instruction_pattern.match(line).groups()
        distance = int(colour[1:6], 16)
        match colour[6]:
            case "0": dx, dy = 1, 0
            case "1": dx, dy = 0, 1
            case "2": dx, dy = -1, 0
            case "3": dx, dy = 0, -1

        current_x = current_x + (dx * distance)
        current_y = current_y + (dy * distance)
        vertices.append((current_x, current_y))
        perimeter_length += distance

    # Below is a slightly modified form of Pick's theorem
    # Normally, this is stated as
    # A = i + b/2 - 1
    # A := area
    # i := number of integer points on the interior
    # b := number of integer points on the boundary
    #
    # The number of boundary points is counted above as
    # the vertices are found (perimeter_length). However,
    # based on some reading on the subreddit, it seems that
    # there is still a slight difference between the calculated
    # area and the actual answer. This can be seen in the
    # example, which should return 952408144115 but instead
    # returns 952408144113 (2 fewer than the correct answer).
    # Adding 2 to the calculated area seems to result in the
    # correct answer.

    return int(0.5 * sum(
        (xi * yi1) - (xi1 * yi)
        for (xi, yi), (xi1, yi1) in zip(vertices, vertices[1:])
    )) + int(0.5 * perimeter_length) + 1

def main() -> tuple[str, int]:
    puzzle_input = util.read.as_lines()

    return "The number of cubic metres of lava the lagoon could hold is {}.", solve(puzzle_input)

class AOC_Tests(unittest.TestCase):
    def test_ex1(self):
        return self.assertEqual(solve(["R 6 (#70c710)",
                                       "D 5 (#0dc571)",
                                       "L 2 (#5713f0)",
                                       "D 2 (#d2c081)",
                                       "R 2 (#59c680)",
                                       "D 2 (#411b91)",
                                       "L 5 (#8ceee2)",
                                       "U 2 (#caa173)",
                                       "L 1 (#1b58a2)",
                                       "U 2 (#caa171)",
                                       "R 2 (#7807d2)",
                                       "U 3 (#a77fa3)",
                                       "L 2 (#015232)",
                                       "U 2 (#7a21e3)"]), 952408144115)

run(main)
