#!/usr/bin/env python3

#Advent of Code
#2020 Day 24, Part 1
#Solution by James C. (https://github.com/JamesMCo)

import os, sys
sys.path.append(os.path.abspath("../.."))
import unittest, util.read
from util.tests import run

from collections import defaultdict
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

    for line in puzzle_input:
        steps = re.findall(direction, line)
        coords = follow_steps(steps)
        floor[coords] = not floor[coords]

    return sum(floor.values())

def main():
    puzzle_input = util.read.as_lines()

    tiles = solve(puzzle_input)

    print("The number of tiles left with the black side up is " + str(tiles) + ".")

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
                                       "wseweeenwnesenwwwswnew"]), 10)

run(main)
