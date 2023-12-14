#!/usr/bin/env python3

#Advent of Code
#2023 Day 14, Part 1
#Solution by James C. (https://github.com/JamesMCo)

import os, sys
sys.path.append(os.path.abspath("../.."))
import unittest, util.read
from util.tests import run

import typing as t

def solve(puzzle_input: list[str]) -> int:
    class Rock:
        dish: "Dish"
        x: int
        y: int

        def __init__(self: t.Self, dish: "Dish", x: int, y: int) -> None:
            self.dish = dish
            self.x = x
            self.y = y

        def __str__(self: t.Self) -> str:
            return "?"

        def slide(self: t.Self, dx: int = 0, dy: int = 0) -> None:
            raise NotImplementedError()

        def load(self: t.Self) -> int:
            raise NotImplementedError()

    class RoundRock(Rock):
        @t.override
        def __str__(self: t.Self) -> str:
            return "O"

        @t.override
        def slide(self: t.Self, dx: int = 0, dy: int = 0) -> None:
            old_x = self.x
            old_y = self.y

            moved = False
            while self.dish.is_empty(self.x + dx, self.y + dy):
                self.x += dx
                self.y += dy
                moved = True

            if moved:
                self.dish.register_movement(self, old_x, old_y, self.x, self.y)

        @t.override
        def load(self: t.Self) -> int:
            return self.dish.height - self.y

    class CubeRock(Rock):
        @t.override
        def __str__(self: t.Self) -> str:
            return "#"

        @t.override
        def slide(self: t.Self, dx: int = 0, dy: int = 0) -> None:
            # Cube-shaped rocks stay in place when the dish is tilted
            return

        @t.override
        def load(self: t.Self) -> int:
            # Cube-shaped rocks do not contribute to the load on the dish
            return 0

    class Dish:
        height: int
        width: int
        all_rocks: dict[tuple[int, int], Rock]
        round_rocks: dict[tuple[int, int], Rock]

        def __init__(self: t.Self, grid: list[str]) -> None:
            self.height = len(grid)
            self.width = len(grid[0])
            self.all_rocks = {}
            self.round_rocks = {}

            for y, row in enumerate(grid):
                for x, col in enumerate(row):
                    match col:
                        case "O":
                            rock = RoundRock(self, x, y)
                            self.all_rocks[(x, y)] = rock
                            self.round_rocks[(x, y)] = rock
                        case "#":
                            self.all_rocks[(x, y)] = CubeRock(self, x, y)
                        case ".":
                            pass

        def __str__(self: t.Self) -> str:
            output = [["."] * self.width for _ in range(self.height)]
            for rock in self.all_rocks.values():
                output[rock.y][rock.x] = str(rock)
            return "\n".join("".join(line) for line in output)

        def register_movement(self: t.Self, rock: Rock, old_x: int, old_y: int, new_x: int, new_y: int) -> None:
            del self.all_rocks[(old_x, old_y)]
            del self.round_rocks[(old_x, old_y)]

            self.all_rocks[(new_x, new_y)] = rock
            self.round_rocks[(new_x, new_y)] = rock

        def is_empty(self: t.Self, x: int, y: int) -> bool:
            return 0 <= x < self.width and\
                   0 <= y < self.height and\
                   (x, y) not in self.all_rocks

        def slide(self: t.Self, direction: str) -> t.Self:
            match direction:
                case "north": dx, dy, sort_key =  0, -1, lambda coords:  coords[1]

            for rock_coords in sorted(self.round_rocks, key=sort_key):
                self.round_rocks[rock_coords].slide(dx, dy)
            return self

        def load(self: t.Self) -> int:
            return sum(rock.load() for rock in self.round_rocks.values())

    return Dish(puzzle_input).slide("north").load()

def main() -> tuple[str, int]:
    puzzle_input = util.read.as_lines()

    return "The total load on the north support beams is {}.", solve(puzzle_input)

class AOC_Tests(unittest.TestCase):
    def test_ex1(self):
        return self.assertEqual(solve(["O....#....",
                                       "O.OO#....#",
                                       ".....##...",
                                       "OO.#O....O",
                                       ".O.....O#.",
                                       "O.#..O.#.#",
                                       "..O..#O..O",
                                       ".......O..",
                                       "#....###..",
                                       "#OO..#...."]), 136)

run(main)
