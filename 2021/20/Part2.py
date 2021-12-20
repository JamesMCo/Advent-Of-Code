#!/usr/bin/env python3

#Advent of Code
#2021 Day 20, Part 2
#Solution by James C. (https://github.com/JamesMCo)

import os, sys
sys.path.append(os.path.abspath("../.."))
import unittest, util.read
from util.tests import run

from util.two_d_world import World

def solve(puzzle_input):
    rules = puzzle_input[0]
    image = World(".", True)
    image.load_from_lists(puzzle_input[2:])

    # If rule 0 is a lit pixel, and rule 511 is a dark pixel,
    # then the infinite space will alternate between all on
    # and all off. To simulate this, we can have the default
    # value for an unexplored cell in the World represent
    # whichever state the infinite space should contain. As
    # a result, any values pulled from the World within the
    # unexplored infinite space will contain the correct value.
    # Whether we should do this is determined by the following
    # condition:
    alternates = rules[0] == "#" and rules[-1] == "."

    for step in range(1, 51):
        new_image = []
        for y in range(image.min_y - 1, image.max_y + 2):
            new_row = ""
            for x in range(image.min_x - 1, image.max_x + 2):
                points = ["1" if image[(x+dx, y+dy)] == "#" else "0" for dy in range(-1, 2) for dx in range(-1, 2)]
                new_row += rules[int("".join(points), 2)]
            new_image.append(new_row)
        image = World(".#"[alternates and step % 2], True)
        image.load_from_lists(new_image)

    return len([v for v in image.values() if v == "#"])

def main():
    puzzle_input = util.read.as_lines()

    pixels = solve(puzzle_input)

    print("The number of pixels that are lit in the resulting image is " + str(pixels) + ".")

class AOC_Tests(unittest.TestCase):
    def test_ex1(self):
        return self.assertEqual(solve(["..#.#..#####.#.#.#.###.##.....###.##.#..###.####..#####..#....#..#..##..###..######.###...####..#..#####..##..#.#####...##.#.#..#.##..#.#......#.###.######.###.####...#.##.##..#..#..#####.....#.#....###..#.##......#.....#..#..#..##..#...##.######.####.####.#.#...#.......#..#.#.#...####.##.#......#..#...##.#.##..#...##.#.##..###.#......#.#.......#.#.#.####.###.##...#.....####.#..#..#.##.#....##..#.####....##...##..#...#......#.#.......#.......##..####..#...#.#.#...##..#.#..###..#####........#..####......#..#",
                                       "",
                                       "#..#.",
                                       "#....",
                                       "##..#",
                                       "..#..",
                                       "..###"]), 3351)

run(main)
