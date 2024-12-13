#!/usr/bin/env python3

#Advent of Code
#2024 Day 13, Part 1
#Solution by James C. (https://github.com/JamesMCo)

import os, sys
sys.path.append(os.path.abspath("../.."))
import unittest, util.read
from util.tests import run

from functools import cache
import re

def solve(puzzle_input: list[str]) -> int:
    @cache
    def press_buttons(button_a: tuple[int, int], button_b: tuple[int, int], prize: tuple[int, int], a_presses: int = 0, b_presses: int = 0) -> int:
        if a_presses > 100 or b_presses > 100:
            # Neither button needs to be pressed this many times.
            return 0
        if (button_a[0] * a_presses) + (button_b[0] * b_presses) == prize[0] and (button_a[1] * a_presses) + (button_b[1] * b_presses) == prize[1]:
            return (a_presses * 3) + b_presses
        else:
            if (button_a[0] * (a_presses + 1)) + (button_b[0] * b_presses) <= prize[0] and (button_a[1] * (a_presses + 1)) + (button_b[1] * b_presses) <= prize[1]:
                if (test_a := press_buttons(button_a, button_b, prize, a_presses + 1, b_presses)) > 0:
                    return test_a
            if (button_a[0] * a_presses) + (button_b[0] * (b_presses + 1)) <= prize[0] and (button_a[1] * a_presses) + (button_b[1] * (b_presses + 1)) <= prize[1]:
                if (test_b := press_buttons(button_a, button_b, prize, a_presses, b_presses + 1)) > 0:
                    return test_b
            # Pressing neither button did lead to the prize
            return 0

    def try_machine(button_a: str, button_b: str, prize: str) -> int:
        return press_buttons(
            tuple(map(int, re.fullmatch(r"Button A: X\+(\d+), Y\+(\d+)", button_a).groups())),
            tuple(map(int, re.fullmatch(r"Button B: X\+(\d+), Y\+(\d+)", button_b).groups())),
            tuple(map(int, re.fullmatch(r"Prize: X=(\d+), Y=(\d+)", prize).groups()))
        )

    return sum(try_machine(*puzzle_input[i:i+3]) for i in range(0, len(puzzle_input), 4))

def main() -> tuple[str, int]:
    puzzle_input = util.read.as_lines()

    return "The fewest tokens required to win all possible prizes is {}.", solve(puzzle_input)

class AOC_Tests(unittest.TestCase):
    def test_ex1(self):
        return self.assertEqual(solve(["Button A: X+94, Y+34",
                                       "Button B: X+22, Y+67",
                                       "Prize: X=8400, Y=5400",
                                       "",
                                       "Button A: X+26, Y+66",
                                       "Button B: X+67, Y+21",
                                       "Prize: X=12748, Y=12176",
                                       "",
                                       "Button A: X+17, Y+86",
                                       "Button B: X+84, Y+37",
                                       "Prize: X=7870, Y=6450",
                                       "",
                                       "Button A: X+69, Y+23",
                                       "Button B: X+27, Y+71",
                                       "Prize: X=18641, Y=10279"]), 480)

run(main)
