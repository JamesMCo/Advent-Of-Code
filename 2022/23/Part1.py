#!/usr/bin/env python3

#Advent of Code
#2022 Day 23, Part 1
#Solution by James C. (https://github.com/JamesMCo)

import os, sys
sys.path.append(os.path.abspath("../.."))
import unittest, util.read
from util.tests import run

from collections import defaultdict
from math import inf

def solve(puzzle_input):
    class Elf:
        elves = []
        positions = set()
        proposals = defaultdict(int)
        min_x = min_y = inf
        max_x = max_y = -inf

        directions = [0, 1, 2, 3]
        round_num = 0

        @classmethod
        def round(cls):
            # Proposal phase
            for elf in cls.elves:
                elf.propose()

            # Movement phase
            cls.positions = set()
            cls.min_x = cls.min_y = inf
            cls.max_x = cls.max_y = -inf
            for elf in cls.elves:
                elf.move()

                Elf.positions.add((elf.x, elf.y))
                if elf.x < Elf.min_x: Elf.min_x = elf.x
                if elf.x > Elf.max_x: Elf.max_x = elf.x
                if elf.y < Elf.min_y: Elf.min_y = elf.y
                if elf.y > Elf.max_y: Elf.max_y = elf.y

            # Cleanup
            cls.proposals.clear()
            cls.round_num += 1

        @classmethod
        def get_area(cls):
            return (cls.max_x - cls.min_x + 1) * (cls.max_y - cls.min_y + 1)

        def __init__(self, x, y):
            self.x = x
            self.y = y
            self.proposal = None

            Elf.elves.append(self)
            Elf.positions.add((x, y))
            if x < Elf.min_x: Elf.min_x = x
            if x > Elf.max_x: Elf.max_x = x
            if y < Elf.min_y: Elf.min_y = y
            if y > Elf.max_y: Elf.max_y = y

        def get_neighbours(self):
            return [neighbour for neighbour in [(self.x + dx, self.y + dy) for dx in range(-1, 2) for dy in range(-1, 2) if not (dx == 0 and dy == 0)] if neighbour in Elf.positions]

        def register_proposal(self, next_x, next_y):
            self.proposal = (next_x, next_y)
            Elf.proposals[(next_x, next_y)] += 1

        def propose(self):
            if not (neighbours := self.get_neighbours()):
                return

            for dir_check in range(4):
                match Elf.directions[(Elf.round_num + dir_check) % 4]:
                    case 0:
                        # North
                        if all(not (self.x + dx, self.y - 1) in neighbours for dx in range(-1, 2)):
                            return self.register_proposal(self.x, self.y - 1)
                    case 1:
                        # South
                        if all(not (self.x + dx, self.y + 1) in neighbours for dx in range(-1, 2)):
                            return self.register_proposal(self.x, self.y + 1)
                    case 2:
                        # West
                        if all(not (self.x - 1, self.y + dy) in neighbours for dy in range(-1, 2)):
                            return self.register_proposal(self.x - 1, self.y)
                    case 3:
                        # East
                        if all(not (self.x + 1, self.y + dy) in neighbours for dy in range(-1, 2)):
                            return self.register_proposal(self.x + 1, self.y)

        def move(self):
            if self.proposal != None and Elf.proposals[self.proposal] == 1:
                self.x, self.y = self.proposal
            self.proposal = None

    for y, row in enumerate(puzzle_input):
        for x, col in enumerate(row):
            if col == "#":
                Elf(x, y)

    for r in range(10):
        Elf.round()

    return Elf.get_area() - len(Elf.elves)

def main():
    puzzle_input = util.read.as_lines()

    tiles = solve(puzzle_input)

    print("The number of empty ground tiles that the rectangle contains is " + str(tiles) + ".")

class AOC_Tests(unittest.TestCase):
    def test_ex1(self):
        return self.assertEqual(solve([".....",
                                       "..##.",
                                       "..#..",
                                       ".....",
                                       "..##.",
                                       "....."]), 25)

    def test_ex2(self):
        return self.assertEqual(solve(["....#..",
                                       "..###.#",
                                       "#...#.#",
                                       ".#...##",
                                       "#.###..",
                                       "##.#.##",
                                       ".#..#.."]), 110)

if __name__ == "__main__":
    run(main)
