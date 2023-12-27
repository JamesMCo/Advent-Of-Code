#!/usr/bin/env python3

#Advent of Code
#2023 Day 24, Part 2
#Solution by James C. (https://github.com/JamesMCo)

import os, sys
sys.path.append(os.path.abspath("../.."))
import unittest, util.read
from util.tests import run

from decimal import Decimal
from math import copysign
import re
from time import perf_counter_ns
from util.colour import cyan, green, yellow

def solve(puzzle_input: list[str], print_timings: bool = True) -> int:
    class Hailstone:
        px: int
        py: int
        pz: int
        vx: int
        vy: int
        vz: int

        _equation_2d: tuple[float | None, float | None, float | None] | None

        hailstone_pattern: re.Pattern = re.compile(r"(-?\d+), +(-?\d+), +(-?\d+) +@ +(-?\d+), +(-?\d+), +(-?\d+)")

        def __init__(self: "Hailstone", hailstone_definition: str) -> None:
            self.px, self.py, self.pz, self.vx, self.vy, self.vz = map(int, self.hailstone_pattern.match(hailstone_definition).groups())
            self._equation_2d = None

        def __str__(self: "Hailstone") -> str:
            return f"{self.px}, {self.py}, {self.pz} @ {self.vx}, {self.vy}, {self.vz}"

        def adjust_by_velocity(self: "Hailstone", vx: int, vy: int, vz: int) -> "Hailstone":
            return Hailstone(f"{self.px}, {self.py}, {self.pz} @ {self.vx - vx}, {self.vy - vy}, {self.vz - vz}")

        @property
        def equation_2d(self: "Hailstone") -> tuple[float | None, float | None, float | None]:
            # Tuple of three values
            # Two optional ints (m, c) fitting the equation y = mx + c
            # An optional int representing an equation x = value (vertical line)
            if self._equation_2d is None:
                if self.vx == 0:
                    self._equation_2d = (None, None, self.vx)
                elif self.vy == 0:
                    self._equation_2d = (0, self.py, None)
                else:
                    # Gradient (dy/dx)
                    m = self.vy / self.vx

                    # Intersection with y-axis (x = 0)
                    # y = mx + c
                    # c = y - mx
                    c = self.py - (m * self.px)

                    self._equation_2d = (m, c, None)
            return self._equation_2d

        def test_point_2d(self: "Hailstone", x: float, y: float) -> bool:
            if self.equation_2d[2] is not None:
                # Constant x (vertical line)
                if x == self.equation_2d[2]:
                    if y == self.py:
                        return True
                    elif self.vy > 0:
                        # Positive vy
                        return y > self.py
                    else:
                        return y < self.py
                return False

            if x == self.px and y == self.py:
                return True

            dx = x - self.px
            dy = y - self.py

            return copysign(1, dx) == copysign(1, self.vx) and copysign(1, dy) == copysign(1, self.vy)

        def intersection_point_2d(self: "Hailstone", other: "Hailstone") -> tuple[int, int] | None:
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
            # - Our starting position or in our future
            # - Their starting position or in their future

            our_m, our_c, our_const_x       = self.equation_2d
            their_m, their_c, their_const_x = other.equation_2d

            if our_const_x is not None and their_const_x is not None:
                if our_const_x == their_const_x:
                    return our_const_x, other.py if self.test_point_2d(other.py, our_const_x) else self.py
                else:
                    return None

            elif our_const_x is not None and their_const_x is None:
                intersection_x = our_const_x
                intersection_y = (their_m * intersection_x) + their_c
            elif our_const_x is None and their_const_x is not None:
                intersection_x = their_const_x
                intersection_y = (our_m * intersection_x) + our_c
            else:
                if our_m == their_m:
                    if our_c == their_c:
                        return (other.px, other.py) if self.test_point_2d(other.px, other.py) else (self.px, self.py)
                    else:
                        return None
                intersection_x = (their_c - our_c) / (our_m - their_m)
                intersection_y = (our_m * intersection_x) + our_c

            if self.test_point_2d(intersection_x, intersection_y) and other.test_point_2d(intersection_x, intersection_y):
                return int(intersection_x), int(intersection_y)

        def get_z_for_x_and_y(self: "Hailstone", x: int, y: int) -> int | None:
            if not self.test_point_2d(x, y):
                # Don't intersect with this point
                return None

            if self.vx != 0:
                # x = px + t*vx
                # t = (x - px) / vx
                t = (x - self.px) / self.vx
            else:
                # y = py + t*vy
                # t = (y - py) / vy
                t = (y - self.py) / self.vy

            if t != int(t):
                # Only integer time steps are valid
                return None

            # z = pz + t*vz
            return self.pz + (int(t) * self.vz)

        def intersection_point_3d(self: "Hailstone", other: "Hailstone") -> tuple[int, int, int] | None:
            if intersection := self.intersection_point_2d(other):
                x, y = intersection

                self_z = self.get_z_for_x_and_y(x, y)
                other_z = other.get_z_for_x_and_y(x, y)

                if self_z is not None and other_z is not None and self_z == other_z:
                    return x, y, self_z

        def test_point_3d(self: "Hailstone", x: int, y: int, z: int) -> bool:
            # Assuming that test_point_2d has already been run, and that by
            # running this function there is an x, y coordinate that is valid
            return self.get_z_for_x_and_y(x, y) == z

    hailstones: list[Hailstone] = [Hailstone(line) for line in puzzle_input]
    max_velocity = 0
    while True:
        loop_start = perf_counter_ns()

        for vx in range(-max_velocity, max_velocity + 1):
            for vy in range(-max_velocity, max_velocity + 1):
                for vz in range(-max_velocity, max_velocity + 1):
                    if not any(abs(v) == max_velocity for v in (vx, vy, vz)):
                        continue
                    # Approach found from discussions on the subreddit:
                    # https://www.reddit.com/r/adventofcode/comments/18pptor/comment/kepufsi
                    #
                    # Adjust every hailstone's velocity to discount (vx, vy, vz).
                    # That is to say that we are looking from the frame of
                    # reference of the stone. In a valid solution, all the
                    # hailstones will pass through a single location. That
                    # location is the starting point of the stone we are
                    # throwing.
                    adjusted_hailstones = [hailstone.adjust_by_velocity(vx, vy, vz) for hailstone in hailstones]

                    # Find point where first two hailstones collide
                    target_coord = adjusted_hailstones[0].intersection_point_3d(adjusted_hailstones[1])
                    # If there is an intersection, check whether all hailstones pass through it
                    if target_coord and \
                        all(hailstone.test_point_2d(target_coord[0], target_coord[1]) for hailstone in adjusted_hailstones) and \
                        all(hailstone.test_point_3d(*target_coord) for hailstone in adjusted_hailstones):
                        # If they do, then return that intersection point (as it is the starting point of the stone)
                        return sum(target_coord)
        seconds = Decimal(
            (perf_counter_ns() - loop_start) / 1_000_000_000  # ns -> s by dividing by 10^9
        ).quantize(Decimal("0.001"))
        if print_timings:
            print(f"{cyan(f"Tested all velocities with max absolute magnitude in any axis of")} {yellow(str(max_velocity))} {cyan("in")} {green(f"{seconds}s")}{cyan(".")}")

        max_velocity += 1

def main() -> tuple[str, int]:
    puzzle_input = util.read.as_lines()

    return "The sum of the coordinates of the initial position is {}.", solve(puzzle_input)

class AOC_Tests(unittest.TestCase):
    def test_ex1(self):
        return self.assertEqual(solve(["19, 13, 30 @ -2,  1, -2",
                                       "18, 19, 22 @ -1, -1, -2",
                                       "20, 25, 34 @ -2, -2, -4",
                                       "12, 31, 28 @ -1, -2, -1",
                                       "20, 19, 15 @  1, -5, -3"], False), 47)

run(main, skip_on_ci=True)
