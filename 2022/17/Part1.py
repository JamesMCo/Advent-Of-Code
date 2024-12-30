#!/usr/bin/env python3

#Advent of Code
#2022 Day 17, Part 1
#Solution by James C. (https://github.com/JamesMCo)

import os, sys
sys.path.append(os.path.abspath("../.."))
import unittest, util.read
from util.tests import run

def solve(puzzle_input):
    class Chamber:
        def __init__(self):
            self.grid = {}
            self.height = 0

        def __getitem__(self, key):
            if key in self.grid:
                return self.grid[key]
            elif key[0] == -1 or key[0] == 7:
                if key[1] == 0:
                    return "+"
                else:
                    return "|"
            elif key[1] == 0:
                return "-"
            else:
                return "."

        def __str__(self):
            return "\n".join(["".join(self[(x,y)] for x in range(-1,8)) for y in range(0, self.height+1)][::-1])

        def is_free(self, x, y):
            return 0 <= x <= 6 and y >= 1 and not (x, y) in self.grid

        def place(self, piece, x, y):
            for offset in piece:
                self.grid[(x+offset[0], y+offset[1])] = "#"
            self.height = max(self.height, y)

    def jets():
        while True:
            for c in puzzle_input:
                yield c

    def pieces(limit=None):
        # Yields tuples of (height, coords of rocks)
        flat = (1, ((0,0), (1, 0), (2, 0), (3, 0)))
        plus = (3, ((1,0), (0,-1), (1,-1), (2,-1), (1,-2)))
        j    = (3, ((2,0), (2,-1), (0,-2), (1,-2), (2,-2)))
        i    = (4, ((0,0), (0,-1), (0,-2), (0,-3)))
        o    = (2, ((0,0), (1, 0), (0,-1), (1,-1)))

        count = 0
        while True:
            for piece in [flat, plus, j, i, o]:
                yield piece
                if (count := count + 1) == limit:
                    return

    chamber = Chamber()
    jet_pattern = jets()
    for piece_height, piece in pieces(2022):
        x = 2
        y = chamber.height + 3 + piece_height
        
        settled = False
        while not settled:
            for (dx, dy) in ((-1 if next(jet_pattern) == "<" else 1, 0), (0, -1)):
                if all(chamber.is_free(x+px+dx, y+py+dy) for px, py in piece):
                    x += dx
                    y += dy
                elif dy == -1:
                    chamber.place(piece, x, y)
                    settled = True

    return chamber.height

def main():
    puzzle_input = util.read.as_string()

    height = solve(puzzle_input)

    print("The height of the tower after 2022 rocks have stopped falling is " + str(height) + ".")

class AOC_Tests(unittest.TestCase):
    def test_ex1(self):
        return self.assertEqual(solve(">>><<><>><<<>><>>><<<>>><<<><<<>><>><<>>"), 3068)

if __name__ == "__main__":
    run(main)
