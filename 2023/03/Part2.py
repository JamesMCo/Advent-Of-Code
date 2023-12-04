#!/usr/bin/env python3

#Advent of Code
#2023 Day 3, Part 2
#Solution by James C. (https://github.com/JamesMCo)

import os, sys
sys.path.append(os.path.abspath("../.."))
import unittest, util.read
from util.tests import run

from collections import defaultdict
import typing as t

def solve(puzzle_input):
    width  = len(puzzle_input[0])
    height = len(puzzle_input)

    class Number:
        x: int
        y: int
        value: int
        length: int

        def __init__(self: t.Self, start_x: int, start_y: int) -> None:
            self.x = start_x
            self.y = start_y
            self.length = 1

            while self.x + self.length < width and puzzle_input[self.y][self.x + self.length].isdigit():
                self.length += 1

            self.value = int(puzzle_input[self.y][self.x : self.x+self.length])

        def adjacent_coords(self: t.Self) -> t.Iterable[tuple[int, int]]:
            for dx in range(-1, self.length + 1):
                if not (0 <= self.x + dx < width):
                    continue

                if self.y > 0:
                    yield self.x + dx, self.y - 1
                yield self.x + dx, self.y
                if self.y < height - 1:
                    yield self.x + dx, self.y + 1

        def adjacent_gears(self: t.Self) -> t.Iterable[tuple[int, int]]:
            for coord in self.adjacent_coords():
                if puzzle_input[coord[1]][coord[0]] == "*":
                    yield coord

    def parse_numbers() -> t.Iterable[Number]:
        for y in range(len(puzzle_input)):
            x = 0
            while x < width:
                if puzzle_input[y][x].isdigit():
                    num = Number(x, y)
                    yield num
                    x += num.length
                else:
                    x += 1

    gears: defaultdict[tuple[int, int], list[Number]] = defaultdict(list)
    for n in parse_numbers():
        for gear in n.adjacent_gears():
            gears[gear].append(n)

    return sum(
        a.value * b.value
        for a, b in filter(
            lambda ns: len(ns) == 2,
            gears.values()
        )
    )

def main():
    puzzle_input = util.read.as_lines()

    return "The sum of all of the gear ratios is {}.", solve(puzzle_input)

class AOC_Tests(unittest.TestCase):
    def test_ex1(self):
        return self.assertEqual(solve(["467..114..",
                                       "...*......",
                                       "..35..633.",
                                       "......#...",
                                       "617*......",
                                       ".....+.58.",
                                       "..592.....",
                                       "......755.",
                                       "...$.*....",
                                       ".664.598.."]), 467835)

run(main)
