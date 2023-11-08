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

    def search(start, step):
        x, y = 0, start
        # The start of the next row is never to the left of the current row
        start_of_row = 0

        while True:
            while get(x, y) == ".":
                x += 1
            start_of_row = x

            while True:
                if get(x, y) == ".":
                    break

                # After reading some discussions on /r/AdventOfCode, I realised
                # that the entire row and column don't need to be checked, only
                # the ends (as there won't be a break in the middle of a row/col)
                # (Reduced runtime from ~66s to ~40s on my machine)

                if get(x + 99, y) == "#":
                    # Split row/col checks, so can skip to next row faster if
                    # the row is no longer wide enough to fit the square
                    # (Reduced runtime from ~40s to ~31s)
                    if get(x, y + 99) == "#":
                        if step == 100:
                            # Coarse search, return result of fine search
                            return search(y - 100, 1)
                        else:
                            # Fine search
                            return (x * 10000) + y
                else:
                    # The row is no longer wide enough to fit the square
                    # Skip to the next row
                    break

                x += 1

            # In the majority of cases, we won't need this row
            # again, as we always look forwards into the grid
            del grid[y]
            x, y = start_of_row, y + step


    # Perform a coarse search by skipping 100 rows at a time
    # Then, backtrack 100 rows and search one row at a time
    # to find the final answer

    # A visual inspection of Part 1 shows that the tractor beam
    # is not wide enough to contain the square
    # This, combined with the gap in the beam in the first few rows
    # means we can start a few rows later

    return search(100, 100)

def main():
    puzzle_input = util.read.as_int_list(",")

    value = solve(puzzle_input)

    print("The value of the closest coordinate in the 100x100 square is " + str(value) + ".")

class AOC_Tests(unittest.TestCase):
    @unittest.skip("No test cases")
    def test_ex1(self):
        pass

run(main)
