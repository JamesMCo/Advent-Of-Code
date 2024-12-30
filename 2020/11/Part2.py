#!/usr/bin/env python3

#Advent of Code
#2020 Day 11, Part 2
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

    def look_for_seat(x, y, dx, dy):
        if world.in_bounds(x, y):
            if (x, y) in world.keys():
                return (x, y)
            return look_for_seat(x + dx, y + dy, dx, dy)
        return None

    # Precalculate lines of sight
    visible_seats = {}
    for x, y in world.keys():
        visible_seats[(x, y)] = [result for dx, dy in vectors if (result := look_for_seat(x + dx, y + dy, dx, dy))]

    def visible(x, y):
        return sum(world[(check_x, check_y)] == "#" for check_x, check_y in visible_seats[(x, y)])

    def step():
        output = {}
        changed = False
        for x, y in world.keys():
            seen_seats = visible(x, y)
            if world[(x, y)] == "L" and seen_seats == 0:
                output[(x, y)] = "#"
                changed = True
            elif world[(x, y)] == "#" and seen_seats >= 5:
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
                                       "L.LLLLL.LL"]), 26)

if __name__ == "__main__":
    run(main)
