#!/usr/bin/env python3

#Advent of Code
#2023 Day 24, Part 1
#Solution by James C. (https://github.com/JamesMCo)

import os, sys
sys.path.append(os.path.abspath("../.."))
import unittest, util.read
from util.tests import run

from itertools import combinations
from math import copysign
import re

def solve(puzzle_input: list[str], min_pos: int = 200_000_000_000_000, max_pos: int = 400_000_000_000_000) -> int:
    class Hailstone:
        px: int
        py: int
        pz: int
        vx: int
        vy: int
        vz: int

        _equation: tuple[float | None, float | None, float | None] | None

        hailstone_pattern: re.Pattern = re.compile(r"(-?\d+), +(-?\d+), +(-?\d+) +@ +(-?\d+), +(-?\d+), +(-?\d+)")

        def __init__(self: "Hailstone", hailstone_definition: str) -> None:
            self.px, self.py, self.pz, self.vx, self.vy, self.vz = map(int, self.hailstone_pattern.match(hailstone_definition).groups())
            self._equation = None

        def __str__(self: "Hailstone") -> str:
            return f"{self.px}, {self.py}, {self.pz} @ {self.vx}, {self.vy}, {self.vz}"

        @property
        def equation_2d(self: "Hailstone") -> tuple[float | None, float | None, float | None]:
            # Tuple of three values
            # Two optional ints (m, c) fitting the equation y = mx + c
            # An optional int representing an equation x = value (vertical line)
            if self._equation is None:
                if self.vx == 0:
                    self._equation = (None, None, self.vx)
                elif self.vy == 0:
                    self._equation = (0, self.py, None)
                else:
                    # Gradient (dy/dx)
                    m = self.vy / self.vx

                    # Intersection with y-axis (x = 0)
                    # y = mx + c
                    # c = y - mx
                    c = self.py - (m * self.px)

                    self._equation = (m, c, None)
            return self._equation

        def test_point_2d(self: "Hailstone", x: float, y: float) -> bool:
            if self.equation_2d[2] is not None:
                # Constant x (vertical line)
                return x == self.equation_2d[2]

            if x == self.px and y == self.py:
                return True

            dx = x - self.px
            dy = y - self.py

            return copysign(1, dx) == copysign(1, self.vx) and copysign(1, dy) == copysign(1, self.vy)

        def intersects_2d(self: "Hailstone", other: "Hailstone") -> bool:
            # General approach:
            # Get y = mx + c for self
            # Get y = mx + c for other
            # If both gradients are equal and the intersects are not equal, they do not intersect
            # If both gradients are equal and the intersects are equal, they are the same line and so intersect
            #
            # Test for intersection by setting equations equal to each other and rearranging for x, then calculating y:
            # (https://en.wikipedia.org/wiki/Line%E2%80%93line_intersection#Given_two_line_equations)
            # ((om, oc) for ours, (tm, tc) for theirs)
            # omx + oc = tmx + tc
            # omx - tmx = tc - oc
            # x(om - tm) = tc - oc
            # x = (tc - oc) / (om - tm)
            # y = om * ((tc - oc) / (om - tm)) + oc
            #
            # Check whether the intersection is:
            # - In the test area
            # - Our starting position or in our future
            # - Their starting position or in their future

            our_m, our_c, our_const_x       = self.equation_2d
            their_m, their_c, their_const_x = other.equation_2d

            if our_const_x is not None and their_const_x is not None:
                return our_const_x == their_const_x

            elif our_const_x is not None and their_const_x is None:
                intersection_x = our_const_x
                intersection_y = (their_m * intersection_x) + their_c
            elif our_const_x is None and their_const_x is not None:
                intersection_x = their_const_x
                intersection_y = (our_m * intersection_x) + our_c
            else:
                if our_m == their_m:
                    return our_c == their_c
                intersection_x = (their_c - our_c) / (our_m - their_m)
                intersection_y = (our_m * intersection_x) + our_c

            if not (min_pos <= intersection_x <= max_pos and min_pos <= intersection_y <= max_pos):
                return False

            return self.test_point_2d(intersection_x, intersection_y) and other.test_point_2d(intersection_x, intersection_y)

    return sum(1 for a, b in combinations((Hailstone(line) for line in puzzle_input), 2) if a.intersects_2d(b))

def main() -> tuple[str, int]:
    puzzle_input = util.read.as_lines()

    return "The number of intersecting hailstone paths in the test area is {}.", solve(puzzle_input)

class AOC_Tests(unittest.TestCase):
    def test_ex1(self):
        return self.assertEqual(solve(["19, 13, 30 @ -2,  1, -2",
                                       "18, 19, 22 @ -1, -1, -2",
                                       "20, 25, 34 @ -2, -2, -4",
                                       "12, 31, 28 @ -1, -2, -1",
                                       "20, 19, 15 @  1, -5, -3"], 7, 27), 2)

if __name__ == "__main__":
    run(main)
