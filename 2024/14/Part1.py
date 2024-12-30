#!/usr/bin/env python3

#Advent of Code
#2024 Day 14, Part 1
#Solution by James C. (https://github.com/JamesMCo)

import os, sys
sys.path.append(os.path.abspath("../.."))
import unittest, util.read
from util.tests import run

import re

def solve(puzzle_input: list[str], width: int = 101, height: int = 103) -> int:
    robot_pattern: re.Pattern = re.compile(r"p=(-?\d+),(-?\d+) v=(-?\d+),(-?\d+)")

    x_middle: int = int((width - 1) / 2)
    y_middle: int = int((height - 1) / 2)

    top_left_count:  int = 0
    top_right_count: int = 0
    bot_left_count:  int = 0
    bot_right_count: int = 0

    for px, py, vx, vy in map(lambda robot: map(int, re.fullmatch(robot_pattern, robot).groups()), puzzle_input):
        final_x: int = (px + (vx * 100)) % width
        final_y: int = (py + (vy * 100)) % height

        if final_x < x_middle and final_y < y_middle:
            top_left_count += 1
        elif final_x > x_middle and final_y < y_middle:
            top_right_count += 1
        elif final_x < x_middle and final_y > y_middle:
            bot_left_count += 1
        elif final_x > x_middle and final_y > y_middle:
            bot_right_count += 1

    return top_left_count * top_right_count * bot_left_count * bot_right_count

def main() -> tuple[str, int]:
    puzzle_input = util.read.as_lines()

    return "The safety factor after 100 seconds is {}.", solve(puzzle_input)

class AOC_Tests(unittest.TestCase):
    def test_ex1(self):
        return self.assertEqual(solve(["p=0,4 v=3,-3",
                                       "p=6,3 v=-1,-3",
                                       "p=10,3 v=-1,2",
                                       "p=2,0 v=2,-1",
                                       "p=0,0 v=1,3",
                                       "p=3,0 v=-2,-2",
                                       "p=7,6 v=-1,-3",
                                       "p=3,0 v=-1,-2",
                                       "p=9,3 v=2,3",
                                       "p=7,3 v=-1,2",
                                       "p=2,4 v=2,-3",
                                       "p=9,5 v=-3,-3"], 11, 7), 12)

if __name__ == "__main__":
    run(main)
