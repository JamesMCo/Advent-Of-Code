#!/usr/bin/env python3

#Advent of Code
#2023 Day 2, Part 2
#Solution by James C. (https://github.com/JamesMCo)

import os, sys
sys.path.append(os.path.abspath("../.."))
import unittest, util.read
from util.tests import run

from math import prod

def solve(puzzle_input):
    class Game:
        game_id: int
        subsets: list[dict[str, int]]
        needed_cubes: dict[str, int]

        def __init__(self: "Game", description: str) -> None:
            self.game_id = int(description.split(": ")[0].split()[1])
            self.subsets = []
            for subset_description in description.split(": ")[1].split("; "):
                subset_dict = {}
                for cube_description in subset_description.split(", "):
                    amount, colour = cube_description.split()
                    subset_dict[colour] = int(amount)
                self.subsets.append(subset_dict)
            self.needed_cubes = {
                "red":   0,
                "green": 0,
                "blue":  0
            }

        def get_minimum_set_power(self: "Game") -> int:
            for subset in self.subsets:
                for colour, amount in subset.items():
                    self.needed_cubes[colour] = max(self.needed_cubes[colour], amount)
            return prod(self.needed_cubes.values())

    return sum(Game(line).get_minimum_set_power() for line in puzzle_input)

def main():
    puzzle_input = util.read.as_lines()

    print(f"The sum of the power of the minimum sets is {solve(puzzle_input)}.")

class AOC_Tests(unittest.TestCase):
    def test_ex1(self):
        return self.assertEqual(solve(["Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green",
                                       "Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue",
                                       "Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red",
                                       "Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red",
                                       "Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green"]), 2286)

run(main)
