#!/usr/bin/env python3

#Advent of Code
#2021 Day 11, Part 1
#Solution by James C. (https://github.com/JamesMCo)

import os, sys
sys.path.append(os.path.abspath("../.."))
import unittest, util.read
from util.tests import run

def solve(puzzle_input):
    class Octopus:
        def __init__(self, x, y, energy):
            self.energy = energy
            self.coords = (x, y)

            self.neighbours = [(x + dx, y + dy) for dx in range(-1, 2) for dy in range(-1, 2) if not (dx == 0 and dy == 0) and 0 <= x + dx < 10 and 0 <= y + dy < 10]
            self.flashed = False
            self.flash_count = 0

        def step(self):
            self.energy += 1
            if self.energy > 9:
                self.flash()

        def flash(self):
            if not self.flashed:
                self.flashed = True
                self.flash_count += 1
                for nx, ny in self.neighbours:
                    octopuses[ny][nx].step()

        def end_step(self):
            self.flashed = False
            if self.energy > 9:
                self.energy = 0

    octopuses = [[Octopus(x, y, int(o)) for x, o in enumerate(row)] for y, row in enumerate(puzzle_input)]
    for step in range(1, 101):
        [o.step() for row in octopuses for o in row]
        [o.end_step() for row in octopuses for o in row]

    return sum(sum(o.flash_count for o in row) for row in octopuses)

def main():
    puzzle_input = util.read.as_lines()

    flashes = solve(puzzle_input)

    print("The total number of flashes after 100 steps is " + str(flashes) + ".")

class AOC_Tests(unittest.TestCase):
    def test_ex1(self):
        return self.assertEqual(solve(["5483143223",
                                       "2745854711",
                                       "5264556173",
                                       "6141336146",
                                       "6357385478",
                                       "4167524645",
                                       "2176841721",
                                       "6882881134",
                                       "4846848554",
                                       "5283751526"]), 1656)

if __name__ == "__main__":
    run(main)
