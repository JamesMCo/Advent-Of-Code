#!/usr/bin/env python3

#Advent of Code
#2019 Day 19, Part 2
#Solution by James C. (https://github.com/JamesMCo)

import os, sys
sys.path.append(os.path.abspath("../.."))
import unittest, util.read
from util.tests import run

from util.intcode_2019 import IntcodeComputer

def solve(puzzle_input):
    computer = IntcodeComputer().load_memory(puzzle_input)
    grid = {}

    def query(coords):
        computer.reset().queue_inputs(coords)
        while not computer.outputs:
            computer.step()
        result = computer.outputs[0]
        return ".#"[result]

    def get(x, y):
        if y not in grid:
            grid[y] = {}
        try:
            result = grid[y][x]
        except KeyError:
            result = query((x, y))
            grid[y][x] = result
        return result

    # Perform a coarse search by skipping 100 rows at a time
    # Then, backtrack 100 rows and search one row at a time
    # to find the final answer
    fine_search_start = None

    # A visual inspection of Part 1 shows that the tractor beam
    # is not wide enough to contain the square
    # This, combined with the gap in the beam in the first few rows
    # means we can start a few rows later
    x, y = 0, 100
    # The start of the next row is never to the left of the current row
    start_of_row = 0
    while True:
        print(f"row={y}")

        while get(x, y) == ".":
            x += 1
        start_of_row = x

        while True:
            if get(x, y) == ".":
                break
            if all(get(x + dx, y) == "#" for dx in range(100)) and all(get(x, y + dy) == "#" for dy in range(100)):
                fine_search_start = y - 100
                break
            x += 1

        if fine_search_start is not None:
            break

        # In the majority of cases (all but 2, possibly)
        # we won't need this row again, as we always look
        # forwards into the grid
        del grid[y]
        x, y = start_of_row, y + 100

    # Fine search (1 row at a time)
    x, y = 0, fine_search_start
    start_of_row = 0
    while True:
        print(f"row={y}")

        while get(x, y) == ".":
            x += 1
        start_of_row = x

        while True:
            if get(x, y) == ".":
                break
            if all(get(x + dx, y) == "#" for dx in range(100)) and all(get(x, y + dy) == "#" for dy in range(100)):
                return (x * 10000) + y
            x += 1

        del grid[y]
        x, y = start_of_row, y + 1


def main():
    puzzle_input = util.read.as_int_list(",")

    value = solve(puzzle_input)

    print("The value of the closest coordinate in the 100x100 square is " + str(value) + ".")

class AOC_Tests(unittest.TestCase):
    @unittest.skip("No test cases")
    def test_ex1(self):
        pass

run(main)
