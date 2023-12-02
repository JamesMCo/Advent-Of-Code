#!/usr/bin/env python3

#Advent of Code
#2023 Day 2, Part 1
#Solution by James C. (https://github.com/JamesMCo)

import os, sys
sys.path.append(os.path.abspath("../.."))
import unittest, util.read
from util.tests import run

import re
import typing as t

def solve(puzzle_input):
    total_cubes = {
        "red":   12,
        "green": 13,
        "blue":  14
    }

    game_pattern: re.Pattern   = re.compile(r"Game (\d+):")
    subset_pattern: re.Pattern = re.compile(r" (\d+) (\w+)(?:[,;]|$)")

    class Game:
        _description: str
        game_id: int
        subsets: t.Iterable[dict[str, int]]

        def __init__(self: t.Self, description: str) -> None:
            self._description = description
            self.game_id = int(game_pattern.match(description).groups()[0])

        @property
        def subsets(self: t.Self) -> t.Iterable[dict[str, int]]:
            # Implement as a property that yields an iterable so that
            # iteration over the subsets only happens once, rather than
            # once during init and once during possibility checking
            for subset_description in self._description.split(";"):
                yield {colour: int(amount) for amount, colour in subset_pattern.findall(subset_description)}

        def get_id_if_possible(self: t.Self) -> int:
            for subset in self.subsets:
                for colour, amount in subset.items():
                    if total_cubes[colour] < amount:
                        # Too many cubes of a given colour
                        return 0
            # Never encountered too many cubes of a given colour
            return self.game_id

    return sum(Game(line).get_id_if_possible() for line in puzzle_input)

def main():
    puzzle_input = util.read.as_lines()

    print(f"The sum of the IDs of the possible games is {solve(puzzle_input)}.")

class AOC_Tests(unittest.TestCase):
    def test_ex1(self):
        return self.assertEqual(solve(["Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green",
                                       "Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue",
                                       "Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red",
                                       "Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red",
                                       "Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green"]), 8)

run(main)
