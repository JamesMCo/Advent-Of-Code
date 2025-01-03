#!/usr/bin/env python3

#Advent of Code
#2018 Day 20, Part 1
#Solution by James C. (https://github.com/JamesMCo)

import os, sys
sys.path.append(os.path.abspath("../.."))
import unittest, util.read
from util.tests import run

from collections import defaultdict
from math import inf

def solve(puzzle_input):
    grid = defaultdict(lambda: "#")
    branches = []
    x, y = 0, 0
    min_x, max_x = inf, -inf
    min_y, max_y = inf, -inf

    grid["0,0"] = "X"
    for char in puzzle_input[1:-1]:
        if char == "(":
            branches.append((x, y))
        elif char == "|":
            x, y = branches[-1]
        elif char == ")":
            x, y = branches.pop()
        elif char == "N":
            y -= 2
            grid[f"{x},{y}"]   = "."
            grid[f"{x},{y+1}"] = "-"
        elif char == "S":
            y += 2
            grid[f"{x},{y}"]   = "."
            grid[f"{x},{y-1}"] = "-"
        elif char == "E":
            x += 2
            grid[f"{x},{y}"]   = "."
            grid[f"{x-1},{y}"] = "|"
        elif char == "W":
            x -= 2
            grid[f"{x},{y}"]   = "."
            grid[f"{x+1},{y}"] = "|"

        min_x = min(min_x, x-1)
        max_x = max(max_x, x+1)
        min_y = min(min_y, y-1)
        max_y = max(max_y, y+1)

    distances = defaultdict(lambda: None)
    distances["0,0"] = 0
    changed = True
    while changed:
        changed = False
        for y in range(min_y, max_y+1):
            for x in range(min_x, max_x+1):
                if grid[f"{x},{y}"] == "." and distances[f"{x},{y}"] == None:
                    potential = []
                    if distances[f"{x},{y-2}"] != None and grid[f"{x},{y-1}"] == "-":
                        potential.append(distances[f"{x},{y-2}"] + 1)
                    if distances[f"{x},{y+2}"] != None and grid[f"{x},{y+1}"] == "-":
                        potential.append(distances[f"{x},{y+2}"] + 1)
                    if distances[f"{x+2},{y}"] != None and grid[f"{x+1},{y}"] == "|":
                        potential.append(distances[f"{x+2},{y}"] + 1)
                    if distances[f"{x-2},{y}"] != None and grid[f"{x-1},{y}"] == "|":
                        potential.append(distances[f"{x-2},{y}"] + 1)

                    if len(potential) > 0:
                        distances[f"{x},{y}"] = max(potential)
                        changed = True

    furthest = 0
    for y in range(min_y, max_y+1):
        for x in range(min_x, max_x+1):
            if distances[f"{x},{y}"] != None and distances[f"{x},{y}"] > furthest:
                furthest = distances[f"{x},{y}"]
    return furthest

def main():
    puzzle_input = util.read.as_string()

    doors = solve(puzzle_input)

    print("The largest number of doors required to reach a room is " + str(doors) + ".")

class AOC_Tests(unittest.TestCase):
    def test_ex1(self):
        self.assertEqual(solve("^WNE$"), 3)

    def test_ex2(self):
        self.assertEqual(solve("^ENWWW(NEEE|SSE(EE|N))$"), 10)

    def test_ex3(self):
        self.assertEqual(solve("^ENNWSWW(NEWS|)SSSEEN(WNSE|)EE(SWEN|)NNN$"), 18)

    def test_ex4(self):
        self.assertEqual(solve("^ESSWWN(E|NNENN(EESS(WNSE|)SSS|WWWSSSSE(SW|NNNE)))$"), 23)

    def test_ex5(self):
        self.assertEqual(solve("^WSSEESWWWNW(S|NENNEEEENN(ESSSSW(NWSW|SSEN)|WSWWN(E|WWS(E|SS))))$"), 31)

if __name__ == "__main__":
    run(main)
