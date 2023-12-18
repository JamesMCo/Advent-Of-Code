#!/usr/bin/env python3

#Advent of Code
#2023 Day 18, Part 1
#Solution by James C. (https://github.com/JamesMCo)

import os, sys
sys.path.append(os.path.abspath("../.."))
import unittest, util.read
from util.tests import run

from collections import deque
import re

def solve(puzzle_input: list[str]) -> int:
    instruction_pattern: re.Pattern = re.compile(r"([UDLR]) (\d+) \((#[0-9a-f]{6})\)")

    hole: set[tuple[int, int]] = {(0, 0)}
    current_x, current_y = (0, 0)
    min_x, min_y = 0, 0
    max_x, max_y = 0, 0

    for line in puzzle_input:
        direction, distance, colour = instruction_pattern.match(line).groups()
        distance = int(distance)
        match direction:
            case "R": dx, dy = 1, 0
            case "D": dx, dy = 0, 1
            case "L": dx, dy = -1, 0
            case "U": dx, dy = 0, -1

        for steps in range(1, distance + 1):
            hole.add((current_x + (dx * steps), current_y + (dy * steps)))

        current_x += dx * distance
        current_y += dy * distance
        min_x = min(min_x, current_x)
        max_x = max(max_x, current_x)
        min_y = min(min_y, current_y)
        max_y = max(max_y, current_y)

    # Give one cube border on all sides to allow flood fill to not get trapped
    min_x -= 1
    min_y -= 1
    max_x += 1
    max_y += 1

    outside: set[tuple[int, int]] = set()
    queue: deque[tuple[int, int]] = deque([(min_x, min_y)])
    while queue:
        current_x, current_y = queue.popleft()
        outside.add((current_x, current_y))

        for dx, dy in ((1, 0), (0, 1), (-1, 0), (0, -1)):
            if min_x <= current_x + dx <= max_x and min_y <= current_y + dy <= max_y:
                if  (current_x + dx, current_y + dy) not in hole\
                and (current_x + dx, current_y + dy) not in outside\
                and (current_x + dx, current_y + dy) not in queue:
                    queue.append((current_x + dx, current_y + dy))

    total_area = (max_x + 1 - min_x) * (max_y + 1 - min_y)
    outside_area = len(outside)

    return total_area - outside_area

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
                                       "U 2 (#7a21e3)"]), 62)

run(main)
