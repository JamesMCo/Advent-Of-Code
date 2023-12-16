#!/usr/bin/env python3

#Advent of Code
#2023 Day 16, Part 1
#Solution by James C. (https://github.com/JamesMCo)

import os, sys
sys.path.append(os.path.abspath("../.."))
import unittest, util.read
from util.tests import run

def solve(puzzle_input: list[str]) -> int:
    class Contraption:
        layout: list[str]
        width: int
        height: int

        beams: list[tuple[int, int, int, int]]
        seen: list[list[tuple[int, int, int, int]]]
        energised: set[tuple[int, int]]

        def __init__(self: "Contraption", layout: list[str]) -> None:
            self.layout = layout[:]
            self.width = len(self.layout[0])
            self.height = len(self.layout)

            self.beams = [(0, 0, 1, 0)]
            self.seen = [[(0, 0, 1, 0)]]
            self.energised = {(0, 0)}

        def in_bounds(self: "Contraption", x: int, y: int) -> bool:
            return 0 <= x < self.width and 0 <= y < self.height

        def simulate_until_cycle(self: "Contraption") -> None:
            while True:
                new_beams: set[tuple[int, int, int, int]] = set()
                for x, y, dx, dy in self.beams:
                    match (self.layout[y][x], (dx, dy)):
                        case (".", _) | ("|", (0, _)) | ("-", (_, 0)):
                            if self.in_bounds(x + dx, y + dy): new_beams.add((x + dx, y + dy, dx, dy))

                        # Reflect up
                        case ("/", (1, 0)) | ("\\", (-1, 0)):
                            if self.in_bounds(x, y - 1): new_beams.add((x, y - 1, 0, -1))
                        # Reflect right
                        case ("/", (0, -1)) | ("\\", (0, 1)):
                            if self.in_bounds(x + 1, y): new_beams.add((x + 1, y, 1, 0))
                        # Reflect down
                        case ("/", (-1, 0)) | ("\\", (1, 0)):
                            if self.in_bounds(x, y + 1): new_beams.add((x, y + 1, 0, 1))
                        # Reflect left
                        case ("/", (0, 1)) | ("\\", (0, -1)):
                            if self.in_bounds(x - 1, y): new_beams.add((x - 1, y, -1, 0))

                        # Split vertically (no-split case handled in first case)
                        case ("|", _):
                            if self.in_bounds(x, y - 1): new_beams.add((x, y - 1, 0, -1))
                            if self.in_bounds(x, y + 1): new_beams.add((x, y + 1, 0, 1))

                        # Split horizontally (no-split case handled in first case)
                        case ("-", _):
                            if self.in_bounds(x - 1, y): new_beams.add((x - 1, y, -1, 0))
                            if self.in_bounds(x + 1, y): new_beams.add((x + 1, y, 1, 0))

                self.beams = sorted(new_beams)
                if self.beams in self.seen:
                    break
                for x, y, dx, dy in self.beams:
                    self.energised.add((x, y))
                self.seen.append(self.beams[:])

    contraption = Contraption(puzzle_input)
    contraption.simulate_until_cycle()

    return len(contraption.energised)

def main() -> tuple[str, int]:
    puzzle_input = util.read.as_lines()

    return "The number of tiles that end up being energised is {}.", solve(puzzle_input)

class AOC_Tests(unittest.TestCase):
    def test_ex1(self):
        return self.assertEqual(solve([".|...\\....",
                                       "|.-.\\.....",
                                       ".....|-...",
                                       "........|.",
                                       "..........",
                                       ".........\\",
                                       "..../.\\\\..",
                                       ".-.-/..|..",
                                       ".|....-|.\\",
                                       "..//.|...."]), 46)

run(main)
