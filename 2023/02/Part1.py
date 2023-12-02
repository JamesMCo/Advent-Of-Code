#!/usr/bin/env python3

#Advent of Code
#2023 Day 2, Part 1
#Solution by James C. (https://github.com/JamesMCo)

import os, sys
sys.path.append(os.path.abspath("../.."))
import unittest, util.read
from util.tests import run

def solve(puzzle_input):
    total_cubes = {
        "red":   12,
        "green": 13,
        "blue":  14
    }

    class Game:
        game_id: int
        subsets: list[dict[str, int]]

        def __init__(self: "Game", description: str) -> None:
            self.game_id = int(description.split(": ")[0].split()[1])
            self.subsets = []
            for subset_description in description.split(": ")[1].split("; "):
                subset_dict = {}
                for cube_description in subset_description.split(", "):
                    amount, colour = cube_description.split()
                    subset_dict[colour] = int(amount)
                self.subsets.append(subset_dict)

        def get_id_if_possible(self: "Game") -> int:
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
