#!/usr/bin/env python3

#Advent of Code
#2024 Day 13, Part 2
#Solution by James C. (https://github.com/JamesMCo)

import os, sys
sys.path.append(os.path.abspath("../.."))
import unittest, util.read
from util.tests import run

import re
import z3

def solve(puzzle_input: list[str]) -> int:
    def solve_for_buttons(button_a: tuple[int, int], button_b: tuple[int, int], prize: tuple[int, int]) -> int:
        a, b = z3.Ints("a b")

        solver = z3.Solver()
        solver.add(
            ((a * button_a[0]) + (b * button_b[0]) == prize[0]),
            ((a * button_a[1]) + (b * button_b[1]) == prize[1])
        )

        if solver.check(a >= 0, b >= 0) == z3.unsat:
            return 0
        model = solver.model()
        return (model[a].as_long() * 3) + model[b].as_long()

    def try_machine(button_a: str, button_b: str, prize: str) -> int:
        return solve_for_buttons(
            tuple(map(int, re.fullmatch(r"Button A: X\+(\d+), Y\+(\d+)", button_a).groups())),
            tuple(map(int, re.fullmatch(r"Button B: X\+(\d+), Y\+(\d+)", button_b).groups())),
            tuple(map(lambda n: int(n) + 10_000_000_000_000, re.fullmatch(r"Prize: X=(\d+), Y=(\d+)", prize).groups()))
        )

    return sum(try_machine(*puzzle_input[i:i+3]) for i in range(0, len(puzzle_input), 4))

def main() -> tuple[str, int]:
    puzzle_input = util.read.as_lines()

    return "The fewest tokens required to win all possible prizes is {}.", solve(puzzle_input)

class AOC_Tests(unittest.TestCase):
    @unittest.skip("No test cases")
    def test_ex1(self):
        pass

run(main)
