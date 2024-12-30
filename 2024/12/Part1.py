#!/usr/bin/env python3

#Advent of Code
#2024 Day 12, Part 1
#Solution by James C. (https://github.com/JamesMCo)

import os, sys
sys.path.append(os.path.abspath("../.."))
import unittest, util.read
from util.tests import run

from collections import deque
from util.two_d_world import World

def solve(puzzle_input: list[str]) -> int:
    plots: World = World(".")
    plots.load_from_lists(puzzle_input)

    handled: set[tuple[int, int]] = set()

    def find_region_price_from_plot(x: int, y: int) -> int:
        plant: str = plots[(x, y)]
        area: int = 0
        perimeter: int = 0

        queue: deque[tuple[int, int]] = deque([(x, y)])
        while queue:
            current_plot: tuple[int, int] = queue.popleft()
            handled.add(current_plot)
            area += 1
            for dx, dy in [(0, -1), (1, 0), (0, 1), (-1, 0)]:
                neighbour: tuple[int, int] = (current_plot[0] + dx, current_plot[1] + dy)
                if not plots.in_bounds(*neighbour):
                    perimeter += 1
                else:
                    if plots[neighbour] == plant:
                        # Ensure plots are only added to the queue once
                        if neighbour not in handled and neighbour not in queue:
                            queue.append(neighbour)
                    else:
                        perimeter += 1

        return area * perimeter

    return sum(find_region_price_from_plot(x, y) for y in range(plots.min_y, plots.max_y + 1) for x in range(plots.min_x, plots.max_x + 1) if (x, y) not in handled)

def main() -> tuple[str, int]:
    puzzle_input = util.read.as_lines()

    return "The total price of fencing is {}.", solve(puzzle_input)

class AOC_Tests(unittest.TestCase):
    def test_ex1(self):
        return self.assertEqual(solve(["AAAA",
                                       "BBCD",
                                       "BBCC",
                                       "EEEC"]), 140)

    def test_ex2(self):
        return self.assertEqual(solve(["OOOOO",
                                       "OXOXO",
                                       "OOOOO",
                                       "OXOXO",
                                       "OOOOO"]), 772)

    def test_ex3(self):
        return self.assertEqual(solve(["RRRRIICCFF",
                                       "RRRRIICCCF",
                                       "VVRRRCCFFF",
                                       "VVRCCCJFFF",
                                       "VVVVCJJCFE",
                                       "VVIVCCJJEE",
                                       "VVIIICJJEE",
                                       "MIIIIIJJEE",
                                       "MIIISIJEEE",
                                       "MMMISSJEEE"]), 1930)

if __name__ == "__main__":
    run(main)
