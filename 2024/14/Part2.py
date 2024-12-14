#!/usr/bin/env python3

#Advent of Code
#2024 Day 14, Part 2
#Solution by James C. (https://github.com/JamesMCo)

import os, sys
sys.path.append(os.path.abspath("../.."))
import unittest, util.read
from util.tests import run

import os
import re
from typing import Self

def solve(puzzle_input: list[str], width: int = 101, height: int = 103) -> int:
    class Robot:
        robot_pattern: re.Pattern = re.compile(r"p=(-?\d+),(-?\d+) v=(-?\d+),(-?\d+)")

        px: int
        py: int
        vx: int
        vy: int

        def __init__(self: Self, description: str) -> None:
            self.px, self.py, self.vx, self.vy = map(int, re.fullmatch(Robot.robot_pattern, description).groups())

        def move(self: Self) -> None:
            self.px = (self.px + self.vx) % width
            self.py = (self.py + self.vy) % height

    robots: list[Robot] = list(map(Robot, puzzle_input))
    seconds: int = 0

    # Solution determined after stepping through outputs one at a time and some research on the subreddit
    #
    # This isn't a very rigorous approach, but I found that the number of unique positions (individually in x and y)
    # normally hovered around 100, and dropped to < 90 periodically. Therefore, I assumed that when both x and y dropped
    # at the same time, we probably had found the Easter egg.
    while True:
        robot_locs: set[tuple[int, int]] = {(robot.px, robot.py) for robot in robots}
        unique_x: int = len(set(robot[0] for robot in robot_locs))
        unique_y: int = len(set(robot[1] for robot in robot_locs))

        if unique_x < 90 and unique_y < 90:
            return seconds

        for robot in robots:
            robot.move()
        seconds += 1

def main() -> tuple[str, int]:
    puzzle_input = util.read.as_lines()

    return "The fewest number of seconds for the robots to display the Easter egg is {}.", solve(puzzle_input)

class AOC_Tests(unittest.TestCase):
    @unittest.skip("No test cases")
    def test_ex1(self):
        pass

run(main)
