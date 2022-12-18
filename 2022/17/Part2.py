#!/usr/bin/env python3

#Advent of Code
#2022 Day 17, Part 2
#Solution by James C. (https://github.com/JamesMCo)

import os, sys
sys.path.append(os.path.abspath("../.."))
import unittest, util.read
from util.tests import run

def solve(puzzle_input):
    # Part 2 specific changes were written with the help of comments on
    # /r/adventofcode, and this visualisation of the example by /u/Boojum/
    # https://www.reddit.com/r/adventofcode/comments/zo27vf/2022_day_17_part_2_rocks_fall_nobody_dies/
    #
    # I also found this interactive visualisation by /u/simonlydell to be incredibly useful when debugging
    # an off-by-one error at the end (I was dropping one too many pieces)
    # https://lydell.github.io/elm-aoc-template/2022-12-17/ab.html
    # 
    # Frankly, I don't fully understand how I got this solution to work, but it does.
    # Roll on Day 18.

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

        def load_from_string(self, cells):
            cells = [cells[i:i+7] for i in range(0, len(cells), 7)]
            for y, row in enumerate(cells[::-1], 1):
                print(row)
                for x, col in enumerate(row):
                    self.grid[(x,y)] = col
                    self.height = max(self.height, y)

        def is_free(self, x, y):
            return 0 <= x <= 6 and y >= 1 and not (x, y) in self.grid

        def find_top(self, x):
            y = self.height
            while self.is_free(x, y):
                y -= 1
            return y

        def top_rows(self):
            return "".join(["".join(self[(x,y)] for x in range(0,7)) for y in range(self.height-7, self.height+1)][::-1])

        def place(self, piece, x, y):
            for offset in piece:
                self.grid[(x+offset[0], y+offset[1])] = "#"
            self.height = max(self.height, y)

    class Jets:
        def __init__(self):
            self.last_jet_index = -1

        def peek_next_jet_index(self):
            i = self.last_jet_index + 1
            if i == len(puzzle_input):
                i = 0

            return i

        def __next__(self):
            i = self.last_jet_index + 1
            if i == len(puzzle_input):
                i = 0

            self.last_jet_index = i
            return puzzle_input[i]

    class Pieces:
        def __init__(self, limit=None):
            self.limit = limit

            # Yields tuples of (height, coords of rocks)
            self.flat = (1, ((0,0), (1, 0), (2, 0), (3, 0)))
            self.plus = (3, ((1,0), (0,-1), (1,-1), (2,-1), (1,-2)))
            self.j    = (3, ((2,0), (2,-1), (0,-2), (1,-2), (2,-2)))
            self.i    = (4, ((0,0), (0,-1), (0,-2), (0,-3)))
            self.o    = (2, ((0,0), (1, 0), (0,-1), (1,-1)))
            self.pieces = (self.flat, self.plus, self.j, self.i, self.o)

            self.count = 0
            self.last_piece_index = -1

        def peek_next_piece_index(self):
            i = self.last_piece_index + 1
            if i == 5:
                i = 0

            return i

        def __iter__(self):
            while True:
                if self.count == self.limit:
                    return
                i = self.last_piece_index + 1
                if i == 5:
                    i = 0

                self.last_piece_index = i
                yield self.pieces[i]
                self.count += 1

    seen = {}

    chamber = Chamber()
    jet_pattern = Jets()
    piece_pattern = Pieces(1000000000000)
    cycle_length = None
    cycle_height = None
    for piece_height, piece in piece_pattern:
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

                    seen_key = (jet_pattern.peek_next_jet_index(), piece_pattern.peek_next_piece_index(), chamber.top_rows())
                    if seen_key in seen:
                        cycle_length = piece_pattern.count - seen[seen_key][0]
                        cycle_height = chamber.height - seen[seen_key][1]
                    else:
                        seen[seen_key] = (piece_pattern.count, chamber.height, chamber.top_rows())
        if cycle_length:
            break
    
    remaining_pieces = 1000000000000 - seen[seen_key][0]
    
    full_cycles = int(remaining_pieces / cycle_length) - 1
    remaining_pieces = remaining_pieces - (full_cycles * cycle_length)

    fixed_height = seen[seen_key][1] + (full_cycles * cycle_height)

    piece_pattern.count = 1000000000000 - remaining_pieces + 1
    irrelevant_height = chamber.height
    # Pretend the chamber has looped however many times

    for piece_height, piece in piece_pattern:
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

    if chamber.height > irrelevant_height:
        return fixed_height + (chamber.height - irrelevant_height)
    else:
        return fixed_height

def main():
    puzzle_input = util.read.as_string()

    height = solve(puzzle_input)

    print("The height of the tower after 1000000000000 rocks have stopped falling is " + str(height) + ".")

class AOC_Tests(unittest.TestCase):
    def test_ex1(self):
        return self.assertEqual(solve(">>><<><>><<<>><>>><<<>>><<<><<<>><>><<>>"), 1514285714288)

run(main)
