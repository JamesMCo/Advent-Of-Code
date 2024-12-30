#!/usr/bin/env python3

#Advent of Code
#2021 Day 25, Part 1
#Solution by James C. (https://github.com/JamesMCo)

import os, sys
sys.path.append(os.path.abspath("../.."))
import unittest, util.read
from util.tests import run

from util.two_d_world import World

def solve(puzzle_input):
    width  = len(puzzle_input[0])
    height = len(puzzle_input)

    class SeaCucumber:
        def __init__(self, x, y, facing):
            self.x = x
            self.y = y
            self.facing = facing

            self.next_x = x
            self.next_y = y
            self.will_move = False

        def consider_move(self, world):
            if self.facing == ">":
                if world[((self.x + 1) % width), self.y] == ".":
                    self.next_x = (self.x + 1) % width
                    self.will_move = True
            elif self.facing == "v":
                if world[(self.x, (self.y + 1) % height)] == ".":
                    self.next_y = (self.y + 1) % height
                    self.will_move = True

        def move(self, new_world):
            self.x = self.next_x
            self.y = self.next_y
            new_world[(self.x, self.y)] = self.facing
            self.will_move = False

        def register_self(self, new_world):
            new_world[(self.x, self.y)] = self.facing

    world = World(".", True)
    world.load_from_lists(puzzle_input)
    seacucumbers = []
    for (x, y) in world.keys():
        if world[(x, y)] != ".":
            seacucumbers.append(SeaCucumber(x, y, world[(x, y)]))

    steps = 0
    while True:
        steps += 1
        for s in seacucumbers:
            if s.facing == ">":
                s.consider_move(world)
        east_moved = any(s.will_move for s in seacucumbers)
        world.grid.clear()
        for s in seacucumbers:
            if s.facing == ">":
                s.move(world)
            else:
                s.register_self(world)

        for s in seacucumbers:
            if s.facing == "v":
                s.consider_move(world)
        south_moved = any(s.will_move for s in seacucumbers)
        world.grid.clear()
        for s in seacucumbers:
            if s.facing == "v":
                s.move(world)
            else:
                s.register_self(world)

        if not (east_moved or south_moved):
            return steps

def main():
    puzzle_input = util.read.as_lines()

    moves = solve(puzzle_input)

    print("The first step on which no sea cucumbers move is " + str(moves) + ".")

class AOC_Tests(unittest.TestCase):
    def test_ex1(self):
        return self.assertEqual(solve(["v...>>.vv>",
                                       ".vv>>.vv..",
                                       ">>.>v>...v",
                                       ">>v>>.>.v.",
                                       "v>v.vv.v..",
                                       ">.>>..v...",
                                       ".vv..>.>v.",
                                       "v.v..>>v.v",
                                       "....v..v.>"]), 58)

if __name__ == "__main__":
    run(main)
