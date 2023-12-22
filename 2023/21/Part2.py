#!/usr/bin/env python3

#Advent of Code
#2023 Day 21, Part 2
#Solution by James C. (https://github.com/JamesMCo)

import os, sys
sys.path.append(os.path.abspath("../.."))
import unittest, util.read
from util.tests import run

from functools import cache

def solve(puzzle_input: list[str], steps = 26501365) -> int:
    width = len(puzzle_input[0])
    height = len(puzzle_input)
    empty: set[tuple[int, int]] = set()

    for y, row in enumerate(puzzle_input):
        for x, col in enumerate(row):
            match col:
                case "#":
                    pass
                case ".":
                    empty.add((x, y))
                case "S":
                    empty.add((x, y))

    if steps <= 5000:
        # This is basically my approach for part 1, but with a slightly more efficient method
        # of expanding the flood fill (only considering moving away from the start into new cells)
        # Unfortunately, due to the scale of the actual part 2 step count and the fact that the
        # example input doesn't include the channels from the centre leading to the edges, I can't
        # use this, but didn't want to just remove it when there are examples that can be run
        # against it! It was also very useful in being able to generate full solutions to smaller
        # step counts that I could analyse when trying to debug my actual part 2 code!
        locations: set[tuple[int, int]] = set()
        ever_seen: set[tuple[int, int]] = set()

        odd_step_seen: set[tuple[int, int]] = set()
        even_step_seen: set[tuple[int, int]] = set()

        for y, row in enumerate(puzzle_input):
            for x, col in enumerate(row):
                if col == "S":
                    locations.add((x, y))
                    even_step_seen.add((x, y))

        for step in range(1, steps + 1):
            new_locations: set[tuple[int, int]] = set()

            for (x, y) in locations:
                for (dx, dy) in ((0, -1), (1, 0), (0, 1), (-1, 0)):
                    if ((x + dx) % width, (y + dy) % height) in empty and (x + dx, y + dy) not in ever_seen:
                        new_locations.add((x + dx, y + dy))

            ever_seen |= new_locations
            if step % 2 == 0:
                even_step_seen |= new_locations
            else:
                odd_step_seen |= new_locations
            locations = new_locations

        if steps % 2 == 0:
            return len(even_step_seen)
        else:
            return len(odd_step_seen)
    else:
        # Actual part 2 solution, based on some reading on the subreddit
        # There were a number of people that mapped a polynomial to the
        # puzzle, but my approach was to find the types of grid that could
        # exist at the target number of steps:
        # - filled grids of both odd and even polarity, though my odd
        #   and even seem to be flipped compared to most others I could
        #   find on the subreddit,
        # - points of the diamond (i.e. the shapes ^, <, v, and >)
        # - diagonals, of both large and small varieties, since the diagonal
        #   doesn't pass exactly through the corners of the grids
        #
        # Below are notes I made while trying to work out my solution, so
        # apologies if they don't quite make sense!
        #
        #
        # Real inputs have empty rows and columns leading from the
        # starting location straight to the edges of the grid, so
        # when flood-filling, they are going to expand without
        # impedance. This is overall going to create a diamond shape.
        # The diamond is going to look like a number of fully filled
        # grids in the middle (alternating between whether they started
        # on an even step or an odd step), and the edges are going
        # to be either a straight diagonal line (originating from a corner),
        # or a triangle (originating from an edge).
        #
        # The input is 131 cells wide and high, with the S in the centre
        # To reach the edges will take 65 steps. To reach the next edge
        # will take another 131 cells.
        # "Coincidentally", 26501365 = 65 + (131 * 202300), so we can
        # find the number of cells that will be filled after starting
        # in each corner and on each edge, as well as from the centre,
        # and do some maths. (Also, "2023"00. Nice. :-P)

        full_grid_cycles = int((steps - 65) / 131)

        @cache
        def count_locations(start: tuple[int, int], step_count: int) -> int:
            locations: set[tuple[int, int]] = {start}
            for step in range(step_count):
                new_locations: set[tuple[int, int]] = set()

                for (x, y) in locations:
                    for (dx, dy) in ((0, -1), (1, 0), (0, 1), (-1, 0)):
                        if (x + dx, y + dy) in empty:
                            new_locations.add((x + dx, y + dy))

                locations = new_locations

            return len(locations)

        # Middle grids
        middle_odd_locations  = count_locations((65, 65), 65 + 131)
        middle_even_locations = count_locations((65, 65), 65 + (131 * 2))
        # Central grid is an even grid
        # Next ring out (4 grids) is all odd grids
        # Next ring out (8 grids) is all even grids
        # etc.
        middle_odd_grids = full_grid_cycles ** 2
        middle_even_grids = (full_grid_cycles - 1) ** 2


        # Point grids (top, left, bottom, right)
        point_grid_locations = sum(count_locations(location, 130) for location in ((65, 0), (0, 65), (65, 130), (130, 65)))


        # Diagonal grids (starting in a corner)
        # Since the number of cells being traversed does not result in being in the centre but rather the edge,
        # the diagonals do not pass through the grid corners.

        # Number of grids on a single diagonal (not the points) is the distance travelled out - 1 grid
        # (1 grid per column, then -1 to discount the point)
        # These are the grids that have travelled through the larger proportion of the grid
        # Big diagonals are even grids
        diagonal_grid_locations = (full_grid_cycles - 1) * sum(count_locations(location, 64 + 131) for location in ((0, 0), (0, 130), (130, 130), (130, 0)))

        # Number of grids on a single diagonal (not the points) that have travelled through the smaller proportion of the grid
        # is the distance travelled out
        # (1 grid per column, as they always travel up/down into it. Points reflect the line rather than continuing it)
        # Smaller diagonals are odd grids
        diagonal_grid_locations += full_grid_cycles * sum(count_locations(location, 64) for location in ((0, 0), (0, 130), (130, 130), (130, 0)))

        return (middle_even_grids * middle_even_locations) + (middle_odd_grids * middle_odd_locations) + point_grid_locations + diagonal_grid_locations

def main() -> tuple[str, int]:
    puzzle_input = util.read.as_lines()

    return "The number of garden plots that the Elf could reach in exactly 26501365 steps is {}.", solve(puzzle_input)

class AOC_Tests(unittest.TestCase):
    def test_ex1(self):
        return self.assertEqual(solve(["...........",
                                       ".....###.#.",
                                       ".###.##..#.",
                                       "..#.#...#..",
                                       "....#.#....",
                                       ".##..S####.",
                                       ".##..#...#.",
                                       ".......##..",
                                       ".##.#.####.",
                                       ".##..##.##.",
                                       "..........."], 6), 16)

    def test_ex2(self):
        return self.assertEqual(solve(["...........",
                                       ".....###.#.",
                                       ".###.##..#.",
                                       "..#.#...#..",
                                       "....#.#....",
                                       ".##..S####.",
                                       ".##..#...#.",
                                       ".......##..",
                                       ".##.#.####.",
                                       ".##..##.##.",
                                       "..........."], 10), 50)

    def test_ex3(self):
        return self.assertEqual(solve(["...........",
                                       ".....###.#.",
                                       ".###.##..#.",
                                       "..#.#...#..",
                                       "....#.#....",
                                       ".##..S####.",
                                       ".##..#...#.",
                                       ".......##..",
                                       ".##.#.####.",
                                       ".##..##.##.",
                                       "..........."], 50), 1594)

    def test_ex4(self):
        return self.assertEqual(solve(["...........",
                                       ".....###.#.",
                                       ".###.##..#.",
                                       "..#.#...#..",
                                       "....#.#....",
                                       ".##..S####.",
                                       ".##..#...#.",
                                       ".......##..",
                                       ".##.#.####.",
                                       ".##..##.##.",
                                       "..........."], 100), 6536)

    def test_ex5(self):
        return self.assertEqual(solve(["...........",
                                       ".....###.#.",
                                       ".###.##..#.",
                                       "..#.#...#..",
                                       "....#.#....",
                                       ".##..S####.",
                                       ".##..#...#.",
                                       ".......##..",
                                       ".##.#.####.",
                                       ".##..##.##.",
                                       "..........."], 500), 167004)

    def test_ex6(self):
        return self.assertEqual(solve(["...........",
                                       ".....###.#.",
                                       ".###.##..#.",
                                       "..#.#...#..",
                                       "....#.#....",
                                       ".##..S####.",
                                       ".##..#...#.",
                                       ".......##..",
                                       ".##.#.####.",
                                       ".##..##.##.",
                                       "..........."], 1000), 668697)

    def test_ex7(self):
        return self.assertEqual(solve(["...........",
                                       ".....###.#.",
                                       ".###.##..#.",
                                       "..#.#...#..",
                                       "....#.#....",
                                       ".##..S####.",
                                       ".##..#...#.",
                                       ".......##..",
                                       ".##.#.####.",
                                       ".##..##.##.",
                                       "..........."], 5000), 16733044)

run(main)
