#!/usr/bin/env python3

#Advent of Code
#2018 Day 17, Part 1
#Solution by James C. (https://github.com/JamesMCo)

import os, sys
sys.path.append(os.path.abspath("../.."))
import unittest, util.read
from util.tests import run

from collections import defaultdict
from math import inf
import re

min_x = inf
max_x = -inf
min_y = inf
max_y = -inf

def render(scan):
    to_return = ""
    for y in range(min_y, max_y+1):
        for x in range(min_x-1, max_x+2):
            to_return += scan[f"{x},{y}"]
        to_return += "\n"
    return to_return

def enclosed(init_x, y, scan):
    enclosed_left  = False
    enclosed_right = False

    x = init_x
    while x >= min_x and not enclosed_left:
        if scan[f"{x},{y}"] == "#":
            enclosed_left = True
            break
        elif scan[f"{x},{y+1}"] not in "#~":
            break
        x -= 1
    x = init_x
    while x <= max_x and not enclosed_right:
        if scan[f"{x},{y}"] == "#":
            enclosed_right = True
            break
        elif scan[f"{x},{y+1}"] not in "#~":
            break
        x += 1
    return enclosed_left and enclosed_right

def drop_and_settle(init_x, init_y, scan, visited=set()):
    x, y = init_x, init_y

    while scan[f"{x},{y+1}"] not in "#~":
        if scan[f"{x},{y}"] == ".":
            scan[f"{x},{y}"] = "|"
        y += 1
        
        if y > max_y:
            return

    visited.add(f"{x},{y}")
    scan[f"{x},{y}"] = "|"

    if enclosed(x, y, scan):
        fill_x = x
        while scan[f"{fill_x-1},{y}"] != "#":
            fill_x -= 1
        while scan[f"{fill_x},{y}"] != "#":
            scan[f"{fill_x},{y}"] = "~"
            fill_x += 1
    else:
        if scan[f"{x-1},{y}"] not in "#~" and f"{x-1},{y}" not in visited:
            drop_and_settle(x-1, y, scan, visited)
            progressed = True
        if scan[f"{x+1},{y}"] not in "#~" and f"{x+1},{y}" not in visited:
            drop_and_settle(x+1, y, scan, visited)
            progressed = True

def solve(puzzle_input):
    global min_x
    global max_x
    global min_y
    global max_y

    scan = defaultdict(lambda: ".")
    scan["500,0"] = "+"

    single_x = re.compile(r"x=(\d*), y=(\d*)\.\.(\d*)")
    single_y = re.compile(r"y=(\d*), x=(\d*)\.\.(\d*)")

    min_x = inf
    max_x = -inf
    min_y = inf
    max_y = -inf

    for vein in puzzle_input:
        if vein[0] == "x":
            x, y_start, y_end = [int(z) for z in re.match(single_x, vein).group(1, 2, 3)]
            min_y = min(min_y, y_start)
            max_y = max(max_y, y_end)
            min_x = min(min_x, x)
            max_x = max(max_x, x)

            for y in range(y_start, y_end+1):
                scan[f"{x},{y}"] = "#"
        elif vein[0] == "y":
            y, x_start, x_end = [int(z) for z in re.match(single_y, vein).group(1, 2, 3)]
            min_x = min(min_x, x_start)
            max_x = max(max_x, x_end)
            min_y = min(min_y, y)
            max_y = max(max_y, y)

            for x in range(x_start, x_end+1):
                scan[f"{x},{y}"] = "#"

    prev_state = ""
    new_state  = render(scan)
    while prev_state != new_state:
        prev_state = new_state
        drop_and_settle(500, 0, scan, set())
        new_state = render(scan)
    return new_state.count("|") + new_state.count("~") + new_state.count("+")

def main():
    puzzle_input = util.read.as_lines()

    reachable = solve(puzzle_input)

    print("The number of tiles the water can reach is " + str(reachable) + ".")

class AOC_Tests(unittest.TestCase):
    def test_ex1(self):
        self.assertEqual(solve(["x=495, y=2..7",
                                "y=7, x=495..501",
                                "x=501, y=3..7",
                                "x=498, y=2..4",
                                "x=506, y=1..2",
                                "x=498, y=10..13",
                                "x=504, y=10..13",
                                "y=13, x=498..504"]), 57)

if __name__ == "__main__":
    run(main)
