#!/usr/bin/env python3

#Advent of Code
#2020 Day 11, Part 1
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

    def adjacent(x, y):
        total = 0
        for dx, dy in vectors:
            if (x + dx, y + dy) in seat_locations_set:
                total += puzzle_input[(x + dx, y + dy)] == "#"
        return total

    def step():
        output = {}
        changed = False
        for x, y in seat_locations_list:
            neighbours = adjacent(x, y)
            if puzzle_input[(x, y)] == "L" and neighbours == 0:
                output[(x, y)] = "#"
                changed = True
            elif puzzle_input[(x, y)] == "#" and neighbours >= 4:
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
                                       "L.LLLLL.LL"]), 37)

run(main)
