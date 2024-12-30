#!/usr/bin/env python3

#Advent of Code
#2023 Day 15, Part 2
#Solution by James C. (https://github.com/JamesMCo)

import os, sys
sys.path.append(os.path.abspath("../.."))
import unittest, util.read
from util.tests import run

from functools import cache
import typing as t

def solve(puzzle_input: list[str]) -> int:
    class Box:
        number: int
        lenses: list[tuple[str, int]]

        def __init__(self: t.Self, number: int) -> None:
            self.number = number
            self.lenses = []

        def remove_lens(self: t.Self, label: str) -> None:
            for i, lens in enumerate(self.lenses):
                if lens[0] == label:
                    self.lenses.pop(i)
                    break

        def add_lens(self: t.Self, label: str, focal_length: int) -> None:
            for i, lens in enumerate(self.lenses):
                if lens[0] == label:
                    self.lenses[i] = (label, focal_length)
                    break
            else:
                self.lenses.append((label, focal_length))

        def focussing_power_of_lenses(self: t.Self) -> int:
            return sum(
                (self.number + 1) * slot * focal_length
                for slot, (_, focal_length) in enumerate(self.lenses, 1)
            )

    @cache
    def HASH(s) -> int:
        current_value = 0
        for c in s:
            current_value = ((current_value + ord(c)) * 17) % 256
        return current_value

    boxes = [Box(n) for n in range(256)]

    for instruction in puzzle_input:
        match instruction[-1]:
            case "-":
                boxes[HASH(instruction[:-1])].remove_lens(instruction[:-1])
            case _:
                boxes[HASH(instruction[:-2])].add_lens(instruction[:-2], int(instruction[-1]))

    return sum(box.focussing_power_of_lenses() for box in boxes)

def main() -> tuple[str, int]:
    puzzle_input = util.read.as_string_list(",")

    return "The focussing power of the resulting lens configuration is {}.", solve(puzzle_input)

class AOC_Tests(unittest.TestCase):
    def test_ex1(self):
        return self.assertEqual(solve(["rn=1", "cm-", "qp=3", "cm=2", "qp-", "pc=4", "ot=9", "ab=5", "pc-", "pc=6", "ot=7"]), 145)

if __name__ == "__main__":
    run(main)
