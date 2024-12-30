#!/usr/bin/env python3

#Advent of Code
#2020 Day 11, Part 1
#Solution by James C. (https://github.com/JamesMCo)

import os, sys
sys.path.append(os.path.abspath("../.."))
import unittest, util.read
from util.tests import run

import util.two_d_world

def solve(puzzle_input):
    vectors = [(0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1), (-1, 0), (-1, 1)]
    world = util.two_d_world.World(".")
    world.load_from_lists(puzzle_input, filter_func=lambda x: x != ".")

    # Precalculate neighbours
    neighbour_seats = {}
    for x, y in world.keys():
        neighbour_seats[(x, y)] = [(x + dx, y + dy) for dx, dy in vectors if (x + dx, y + dy) in world.keys()]

    def adjacent(x, y):
        return sum(world[(check_x, check_y)] == "#" for check_x, check_y in neighbour_seats[(x, y)])

    def step():
        output = {}
        changed = False
        for x, y in world.keys():
            neighbours = adjacent(x, y)
            if world[(x, y)] == "L" and neighbours == 0:
                output[(x, y)] = "#"
                changed = True
            elif world[(x, y)] == "#" and neighbours >= 4:
                output[(x, y)] = "L"
                changed = True
            else:
                output[(x, y)] = world[(x, y)]
        return output, changed

    while True:
        new_state, changed = step()
        if not changed:
            return sum(seat == "#" for seat in world.values())
        world.load_from_dict(new_state)

def main():
    puzzle_input = util.read.as_lines()

    seats = solve(puzzle_input)

    print("The number of occupied seats is " + str(seats) + ".")

class AOC_Tests(unittest.TestCase):
    def test_ex1(self):
        return self.assertEqual(solve(["L.LL.LL.LL",
                                       "LLLLLLL.LL",
                                       "L.L.L..L..",
                                       "LLLL.LL.LL",
                                       "L.LL.LL.LL",
                                       "L.LLLLL.LL",
                                       "..L.L.....",
                                       "LLLLLLLLLL",
                                       "L.LLLLLL.L",
                                       "L.LLLLL.LL"]), 37)

if __name__ == "__main__":
    run(main)
