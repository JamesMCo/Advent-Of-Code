#!/usr/bin/env python3

#Advent of Code
#2023 Day 24, Part 2
#Solution by James C. (https://github.com/JamesMCo)

import os, sys
sys.path.append(os.path.abspath("../.."))
import unittest, util.read
from util.tests import run

import re
import z3

def solve(puzzle_input: list[str]) -> int:
    class Hailstone:
        px: int
        py: int
        pz: int
        vx: int
        vy: int
        vz: int

        hailstone_pattern: re.Pattern = re.compile(r"(-?\d+), +(-?\d+), +(-?\d+) +@ +(-?\d+), +(-?\d+), +(-?\d+)")

        def __init__(self: "Hailstone", hailstone_definition: str) -> None:
            self.px, self.py, self.pz, self.vx, self.vy, self.vz = map(int, self.hailstone_pattern.match(hailstone_definition).groups())
            self._equation_2d = None

        def __str__(self: "Hailstone") -> str:
            return f"{self.px}, {self.py}, {self.pz} @ {self.vx}, {self.vy}, {self.vz}"

    px, py, pz = z3.Reals("px py pz")
    vx, vy, vz = z3.Reals("vx vy vz")
    t = [z3.Real(f"t{i}") for i in range(len(puzzle_input))]
    equations = [
        (
            hailstone.px + (hailstone.vx * t[i]) == px + (vx * t[i]),
            hailstone.py + (hailstone.vy * t[i]) == py + (vy * t[i]),
            hailstone.pz + (hailstone.vz * t[i]) == pz + (vz * t[i])
        )
        for i, hailstone in enumerate(Hailstone(line) for line in puzzle_input)
    ]

    solver = z3.Solver()
    for hailstone_equations in equations:
        # Only three hailstones are needed to be able to
        # solve the set of equations (9 unknowns in 9 equations)
        # but there doesn't seem to be any harm from some quick
        # testing in including all the hailstones.
        solver.add(*hailstone_equations)

    # Find values that solve the equations
    solver.check()
    model = solver.model()

    # Sum the values of the initial location px, py, and pz
    return sum(model[value].as_long() for value in (px, py, pz))

def main() -> tuple[str, int]:
    puzzle_input = util.read.as_lines()

    return "The sum of the coordinates of the initial position is {}.", solve(puzzle_input)

class AOC_Tests(unittest.TestCase):
    def test_ex1(self):
        return self.assertEqual(solve(["19, 13, 30 @ -2,  1, -2",
                                       "18, 19, 22 @ -1, -1, -2",
                                       "20, 25, 34 @ -2, -2, -4",
                                       "12, 31, 28 @ -1, -2, -1",
                                       "20, 19, 15 @  1, -5, -3"]), 47)

run(main)
