#!/usr/bin/env python3

#Advent of Code
#2024 Day 12, Part 2
#Solution by James C. (https://github.com/JamesMCo)

import os, sys
sys.path.append(os.path.abspath("../.."))
import unittest, util.read
from util.tests import run

from collections import defaultdict, deque
from util.two_d_world import World

def solve(puzzle_input: list[str]) -> int:
    plots: World = World(".")
    plots.load_from_lists(puzzle_input)

    handled: set[tuple[int, int]] = set()

    def find_sides_of_region(region_plots: set[tuple[int, int]], boundary_plots: set[tuple[int, int]]) -> int:
        # Boundaries are considered looking from non-region plots into region plots
        # List order is [up, right, down, left]
        boundary_types: defaultdict[tuple[int, int], list[bool]] = defaultdict(lambda: [False] * 4)

        for plot in boundary_plots:
            # Plot up from current plot
            if (plot[0], plot[1] - 1) not in region_plots:
                boundary_types[(plot[0], plot[1] - 1)][2] = True
            # Plot right from current plot
            if (plot[0] + 1, plot[1]) not in region_plots:
                boundary_types[(plot[0] + 1, plot[1])][3] = True
            # Plot down from current plot
            if (plot[0], plot[1] + 1) not in region_plots:
                boundary_types[(plot[0], plot[1] + 1)][0] = True
            # Plot left from current plot
            if (plot[0] - 1, plot[1]) not in region_plots:
                boundary_types[(plot[0] - 1, plot[1])][1] = True

        min_x: int = min([plot[0] for plot in boundary_types])
        max_x: int = max([plot[0] for plot in boundary_types])
        min_y: int = min([plot[1] for plot in boundary_types])
        max_y: int = max([plot[1] for plot in boundary_types])

        sides: int = 0

        # Scanning left to right looking for "up" and "down" sides
        for y in range(min_y, max_y + 1):
            in_side_up: bool = False
            in_side_down: bool = False
            for x in range(min_x, max_x + 1):
                if (x, y) in boundary_types:
                    if boundary_types[(x, y)][0]:
                        # There is an "up" side
                        if in_side_up:
                            # This is a continuation of an "up" side
                            if boundary_types[(x, y)][1]:
                                # However, there is a "right" side here which cuts off the "up" side
                                in_side_up = False
                            else:
                                # The "up" side continues, and so we don't need to do anything
                                pass
                        else:
                            # We've just entered an "up" side, so track it
                            sides += 1
                            in_side_up = True
                    else:
                        # There is no "up" side. We might already know this, but better safe than sorry.
                        in_side_up = False

                    if boundary_types[(x, y)][2]:
                        # There is a "down" side
                        if in_side_down:
                            # This is a continuation of a "down" side
                            if boundary_types[(x, y)][1]:
                                # However, there is a "right" side here which cuts off the "down" side
                                in_side_down = False
                            else:
                                # The "down" side continues, and so we don't need to do anything
                                pass
                        else:
                            # We've just entered a "down" side, so track it
                            sides += 1
                            in_side_down = True
                    else:
                        # There is no "down" side. We might already know this, but better safe than sorry.
                        in_side_down = False
                else:
                    # This plot has no boundary, and so definitely has no "up" or "down" side
                    in_side_up = False
                    in_side_down = False

        # Scanning top to bottom looking for "left" and "right" sides
        for x in range(min_x, max_x + 1):
            in_side_left: bool = False
            in_side_right: bool = False
            for y in range(min_y, max_y + 1):
                if (x, y) in boundary_types:
                    if boundary_types[(x, y)][3]:
                        # There is a "left" side
                        if in_side_left:
                            # This is a continuation of a "left" side
                            if boundary_types[(x, y)][2]:
                                # However, there is a "down" side here which cuts off the "left" side
                                in_side_left = False
                            else:
                                # The "left" side continues, and so we don't need to do anything
                                pass
                        else:
                            # We've just entered a "left" side, so track it
                            sides += 1
                            in_side_left = True
                    else:
                        # There is no "left" side. We might already know this, but better safe than sorry.
                        in_side_left = False

                    if boundary_types[(x, y)][1]:
                        # There is a "right" side
                        if in_side_right:
                            # This is a continuation of a "right" side
                            if boundary_types[(x, y)][2]:
                                # However, there is a "down" side here which cuts off the "right" side
                                in_side_right = False
                            else:
                                # The "right" side continues, and so we don't need to do anything
                                pass
                        else:
                            # We've just entered a "right" side, so track it
                            sides += 1
                            in_side_right = True
                    else:
                        # There is no "right" side. We might already know this, but better safe than sorry.
                        in_side_right = False
                else:
                    # This plot has no boundary, and so definitely has no "left" or "right" side
                    in_side_left = False
                    in_side_right = False

        return sides

    def find_region_price_from_plot(x: int, y: int) -> int:
        plant: str = plots[(x, y)]
        region_plots: set[tuple[int, int]] = set()
        boundary_plots: set[tuple[int, int]] = set()

        queue: deque[tuple[int, int]] = deque([(x, y)])
        while queue:
            current_plot: tuple[int, int] = queue.popleft()
            handled.add(current_plot)
            region_plots.add(current_plot)
            for dx, dy in [(0, -1), (1, 0), (0, 1), (-1, 0)]:
                neighbour: tuple[int, int] = (current_plot[0] + dx, current_plot[1] + dy)
                if not plots.in_bounds(*neighbour):
                    boundary_plots.add(current_plot)
                else:
                    if plots[neighbour] == plant:
                        # Ensure plots are only added to the queue once
                        if neighbour not in handled and neighbour not in queue:
                            queue.append(neighbour)
                    else:
                        boundary_plots.add(current_plot)

        return len(region_plots) * find_sides_of_region(region_plots, boundary_plots)

    return sum(find_region_price_from_plot(x, y) for y in range(plots.min_y, plots.max_y + 1) for x in range(plots.min_x, plots.max_x + 1) if (x, y) not in handled)

def main() -> tuple[str, int]:
    puzzle_input = util.read.as_lines()

    return "The total price of fencing is {}.", solve(puzzle_input)

class AOC_Tests(unittest.TestCase):
    def test_ex1(self):
        return self.assertEqual(solve(["AAAA",
                                       "BBCD",
                                       "BBCC",
                                       "EEEC"]), 80)

    def test_ex2(self):
        return self.assertEqual(solve(["OOOOO",
                                       "OXOXO",
                                       "OOOOO",
                                       "OXOXO",
                                       "OOOOO"]), 436)

    def test_ex3(self):
        return self.assertEqual(solve(["EEEEE",
                                       "EXXXX",
                                       "EEEEE",
                                       "EXXXX",
                                       "EEEEE"]), 236)

    def test_ex4(self):
        return self.assertEqual(solve(["AAAAAA",
                                       "AAABBA",
                                       "AAABBA",
                                       "ABBAAA",
                                       "ABBAAA",
                                       "AAAAAA"]), 368)

    def test_ex5(self):
        return self.assertEqual(solve(["RRRRIICCFF",
                                       "RRRRIICCCF",
                                       "VVRRRCCFFF",
                                       "VVRCCCJFFF",
                                       "VVVVCJJCFE",
                                       "VVIVCCJJEE",
                                       "VVIIICJJEE",
                                       "MIIIIIJJEE",
                                       "MIIISIJEEE",
                                       "MMMISSJEEE"]), 1206)

if __name__ == "__main__":
    run(main)
