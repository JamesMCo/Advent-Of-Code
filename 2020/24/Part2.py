#!/usr/bin/env python3

#Advent of Code
#2020 Day 24, Part 2
#Solution by James C. (https://github.com/JamesMCo)

import os, sys
sys.path.append(os.path.abspath("../.."))
import unittest, util.read
from util.tests import run

from collections import defaultdict
from functools import cache
import math
import re

def solve(puzzle_input):
    direction = re.compile(r"e|se|sw|w|nw|ne")

    floor = defaultdict(bool)

    def follow_steps(steps):
        x = 0.0
        y = 0
        for step in steps:
            if   step == "e":  x += 1.0
            elif step == "se": x, y = x + 0.5, y + 1
            elif step == "sw": x, y = x - 0.5, y + 1
            elif step == "w":  x -= 1.0
            elif step == "nw": x, y = x - 0.5, y - 1
            elif step == "ne": x, y = x + 0.5, y - 1
        return (x, y)

    floor["min_x"] = floor["min_y"] = None
    floor["max_x"] = floor["max_y"] = None
    for line in puzzle_input:
        steps = re.findall(direction, line)
        coords = follow_steps(steps)
        floor[coords] = not floor[coords]

        if floor["min_x"] == None: floor["min_x"] = coords[0]
        else: floor["min_x"] = min(math.floor(floor["min_x"]), coords[0])

        if floor["max_x"] == None: floor["max_x"] = coords[0]
        else: floor["max_x"] = max(math.ceil(floor["max_x"]),  coords[0])

        if floor["min_y"] == None: floor["min_y"] = coords[1]
        else: floor["min_y"] = min(math.floor(floor["min_y"]), coords[1])

        if floor["max_y"] == None: floor["max_y"] = coords[1]
        else: floor["max_y"] = max(math.ceil(floor["max_y"]),  coords[1])

    @cache
    def neighbours(x, y):
        return [(x + dx, y + dy) for dx, dy in [(1.0, 0), (0.5, 1), (-0.5, 1), (-1.0, 0), (-0.5, -1), (0.5, -1)]]

    def day(prev_floor):
        new_floor = defaultdict(bool)
        for y in range(prev_floor["min_y"] - 1, prev_floor["max_y"] + 2):
            for x in range(prev_floor["min_x"] - 1, prev_floor["max_x"] + 2):
                if y % 2 == 1: x = x - 0.5
                else: x = float(x)
                n = sum(prev_floor[(nx, ny)] for nx, ny in neighbours(x, y))
                if prev_floor[(x, y)] and (n == 0 or n > 2):
                    new_floor[(x, y)] = False
                elif (not prev_floor[(x, y)]) and n == 2:
                    new_floor[(x, y)] = True
                else:
                    new_floor[(x, y)] = prev_floor[(x, y)]

        new_floor["min_x"] = prev_floor["min_x"] - 1
        new_floor["max_x"] = prev_floor["max_x"] + 1
        new_floor["min_y"] = prev_floor["min_y"] - 1
        new_floor["max_y"] = prev_floor["max_y"] + 1
        return new_floor

    for d in range(100):
        floor = day(floor)
    return sum(floor.values())

def main():
    puzzle_input = util.read.as_lines()

    tiles = solve(puzzle_input)

    print("The number of tiles left with the black side up after 100 days is " + str(tiles) + ".")

class AOC_Tests(unittest.TestCase):
    def test_ex1(self):
        return self.assertEqual(solve(["sesenwnenenewseeswwswswwnenewsewsw",
                                       "neeenesenwnwwswnenewnwwsewnenwseswesw",
                                       "seswneswswsenwwnwse",
                                       "nwnwneseeswswnenewneswwnewseswneseene",
                                       "swweswneswnenwsewnwneneseenw",
                                       "eesenwseswswnenwswnwnwsewwnwsene",
                                       "sewnenenenesenwsewnenwwwse",
                                       "wenwwweseeeweswwwnwwe",
                                       "wsweesenenewnwwnwsenewsenwwsesesenwne",
                                       "neeswseenwwswnwswswnw",
                                       "nenwswwsewswnenenewsenwsenwnesesenew",
                                       "enewnwewneswsewnwswenweswnenwsenwsw",
                                       "sweneswneswneneenwnewenewwneswswnese",
                                       "swwesenesewenwneswnwwneseswwne",
                                       "enesenwswwswneneswsenwnewswseenwsese",
                                       "wnwnesenesenenwwnenwsewesewsesesew",
                                       "nenewswnwewswnenesenwnesewesw",
                                       "eneswnwswnwsenenwnwnwwseeswneewsenese",
                                       "neswnwewnwnwseenwseesewsenwsweewe",
                                       "wseweeenwnesenwwwswnew"]), 2208)

if __name__ == "__main__":
    run(main)
