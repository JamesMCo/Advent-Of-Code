#!/usr/bin/env python3

#Advent of Code
#2020 Day 11, Part 2
#Solution by James C. (https://github.com/JamesMCo)

import os, sys
sys.path.append(os.path.abspath("../.."))
import unittest, util.read
from util.tests import run

def solve(puzzle_input):
    width  = len(puzzle_input[0])
    height = len(puzzle_input)
    vectors = [(0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1), (-1, 0), (-1, 1)]
    seat_locations_list = [(x, y) for x in range(width) for y in range(height) if puzzle_input[y][x] != "."]
    seat_locations_set  = set(seat_locations_list)

    def in_bounds(axis, coordinate):
        return 0 <= coordinate < (width if axis == "x" else height)

    def look_for_seat(x, y, dx, dy):
        if in_bounds("x", x) and in_bounds("y", y):
            if (x, y) in seat_locations_set:
                return puzzle_input[(x, y)]
            return look_for_seat(x + dx, y + dy, dx, dy)
        return ""

    def visible(x, y):
        total = 0
        for dx, dy in vectors:
            total += look_for_seat(x + dx, y + dy, dx, dy) == "#"
        return total

    def step():
        output = {}
        changed = False
        for x, y in seat_locations_list:
            seen_seats = visible(x, y)
            if puzzle_input[(x, y)] == "L" and seen_seats == 0:
                output[(x, y)] = "#"
                changed = True
            elif puzzle_input[(x, y)] == "#" and seen_seats >= 5:
                output[(x, y)] = "L"
                changed = True
            else:
                output[(x, y)] = puzzle_input[(x, y)]
        return output, changed

    puzzle_input = {(x, y):puzzle_input[y][x] for (x, y) in seat_locations_list}
    while True:
        puzzle_input, changed = step()
        if not changed:
            return sum(puzzle_input[(x, y)] == "#" for x, y in seat_locations_list)

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

run(main)
