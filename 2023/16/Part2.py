#!/usr/bin/env python3

#Advent of Code
#2023 Day 16, Part 2
#Solution by James C. (https://github.com/JamesMCo)

import os, sys
sys.path.append(os.path.abspath("../.."))
import unittest, util.read
from util.tests import run

import typing as t

def solve(puzzle_input: list[str]) -> int:
    class Contraption:
        layout: list[str]
        width: int
        height: int

        beams: list[tuple[int, int, int, int]]
        seen: list[list[tuple[int, int, int, int]]]
        energised: set[tuple[int, int]]

        def __init__(self: t.Self, layout: list[str], initial_beam: tuple[int, int, int, int]) -> None:
            self.layout = layout[:]
            self.width = len(self.layout[0])
            self.height = len(self.layout)

            self.beams = [initial_beam]
            self.seen = [[initial_beam]]
            self.energised = {(initial_beam[0], initial_beam[1])}

        def in_bounds(self: t.Self, x: int, y: int) -> bool:
            return 0 <= x < self.width and 0 <= y < self.height

        def simulate_until_cycle(self: t.Self) -> None:
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

                # debug_map = [list(line) for line in self.layout]
                # for x, y, dx, dy in new_beams:
                #     if debug_map[y][x] in ">v<^":
                #         debug_map[y][x] = "2"
                #     elif debug_map[y][x] in "2345678":
                #         debug_map[y][x] = str(int(debug_map[y][x]) + 1)
                #     elif debug_map[y][x] == "9":
                #         debug_map[y][x] = "X"
                #     else:
                #         match dx, dy:
                #             case 1, 0: debug_map[y][x] = ">"
                #             case 0, 1: debug_map[y][x] = "v"
                #             case -1, 0: debug_map[y][x] = "<"
                #             case 0, -1: debug_map[y][x] = "^"
                # input("\n".join("".join(line) for line in debug_map) + "\n")

                self.beams = sorted(new_beams)
                if self.beams in self.seen:
                    break
                for x, y, dx, dy in self.beams:
                    self.energised.add((x, y))
                self.seen.append(self.beams[:])

    def starting_positions(width: int, height: int) -> t.Iterable[tuple[int, int, int, int]]:
        # Right from left edge
        for y in range(height):
            yield 0, y, 1, 0

        # Down from top edge
        for x in range(width):
            yield x, 0, 0, 1

        # Left from right edge
        for y in range(height):
            yield 0, y, -1, 0

        # Up from bottom edge
        for x in range(width):
            yield x, 0, 0, -1

    def test_starting_position(starting_position: tuple[int, int, int, int]) -> int:
        contraption = Contraption(puzzle_input, starting_position)
        contraption.simulate_until_cycle()
        return len(contraption.energised)

    return max(map(test_starting_position, starting_positions(len(puzzle_input[0]), len(puzzle_input))))

def main() -> tuple[str, int]:
    puzzle_input = util.read.as_lines()

    return "The largest number of tiles that can be energised from any configuration is {}.", solve(puzzle_input)

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
                                       "..//.|...."]), 51)

run(main)
