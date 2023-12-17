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

        def __init__(self: "Contraption", layout: list[str]) -> None:
            self.layout = layout[:]
            self.width = len(self.layout[0])
            self.height = len(self.layout)

        def in_bounds(self: "Contraption", x: int, y: int) -> bool:
            return 0 <= x < self.width and 0 <= y < self.height

        def simulate_until_cycle(self: "Contraption", initial_beam: tuple[int, int, int, int]) -> int:
            # Refactored to use more efficient cycle detection after
            # a conversation with a friend (@Ggrgra on Twitter)
            #
            # Before, I was using the entire state of all beams to
            # detect a cycle, where I only needed to check whether
            # a beam had previously been on a given cell facing in
            # the same direction, and then just don't bother to
            # simulate that beam any further (as it will only ever
            # result in duplicated work and results).

            beams = [initial_beam]
            seen = {initial_beam}
            energised = {(initial_beam[0], initial_beam[1])}

            while True:
                new_beams: set[tuple[int, int, int, int]] = set()
                for x, y, dx, dy in beams:
                    match (self.layout[y][x], (dx, dy)):
                        case (".", _) | ("|", (0, _)) | ("-", (_, 0)):
                            if self.in_bounds(x + dx, y + dy) and (x + dx, y + dy, dx, dy) not in seen:
                                new_beams.add((x + dx, y + dy, dx, dy))

                        # Reflect up
                        case ("/", (1, 0)) | ("\\", (-1, 0)):
                            if self.in_bounds(x, y - 1) and (x, y - 1, 0, -1) not in seen:
                                new_beams.add((x, y - 1, 0, -1))
                        # Reflect right
                        case ("/", (0, -1)) | ("\\", (0, 1)):
                            if self.in_bounds(x + 1, y) and (x + 1, y, 1, 0) not in seen:
                                new_beams.add((x + 1, y, 1, 0))
                        # Reflect down
                        case ("/", (-1, 0)) | ("\\", (1, 0)):
                            if self.in_bounds(x, y + 1) and (x, y + 1, 0, 1) not in seen:
                                new_beams.add((x, y + 1, 0, 1))
                        # Reflect left
                        case ("/", (0, 1)) | ("\\", (0, -1)):
                            if self.in_bounds(x - 1, y) and (x - 1, y, -1, 0) not in seen:
                                new_beams.add((x - 1, y, -1, 0))

                        # Split vertically (no-split case handled in first case)
                        case ("|", _):
                            if self.in_bounds(x, y - 1) and (x, y - 1, 0, -1) not in seen:
                                new_beams.add((x, y - 1, 0, -1))
                            if self.in_bounds(x, y + 1) and (x, y + 1, 0, 1) not in seen:
                                new_beams.add((x, y + 1, 0, 1))

                        # Split horizontally (no-split case handled in first case)
                        case ("-", _):
                            if self.in_bounds(x - 1, y) and (x - 1, y, -1, 0) not in seen:
                                new_beams.add((x - 1, y, -1, 0))
                            if self.in_bounds(x + 1, y) and (x + 1, y, 1, 0) not in seen:
                                new_beams.add((x + 1, y, 1, 0))

                if not new_beams:
                    return len(energised)
                beams = new_beams
                for x, y, dx, dy in beams:
                    energised.add((x, y))
                    seen.add((x, y, dx, dy))

    return Contraption(puzzle_input).simulate_until_cycle((0, 0, 1, 0))

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
