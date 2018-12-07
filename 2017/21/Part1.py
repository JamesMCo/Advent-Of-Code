#!/usr/bin/env python3

#Advent of Code
#Day 21, Part 1
#Solution by James C. (https://github.com/JamesMCo)

import os, sys
sys.path.append(os.path.abspath("../.."))
import unittest, util.read
from util.tests import run

def solve(puzzle_input, iters=5):
    book = [{}, {}]
    grid = [".#.", "..#", "###"]
    new_grid = []

    for line in puzzle_input:
        left  = line.split(" => ")[0].replace("/", "")
        right = line.split(" => ")[1].replace("/", "")
        if line[2] == "/":
            book[0][left] = right
        else:
            book[1][left] = right

    def find_2x2(square):
        for i in range(2):
            for j in range(4):
                if square in book[0]:
                    return book[0][square]
                square = square[1] + square[3] + \
                         square[0] + square[2]

            square = square[1] + square[0] + \
                     square[3] + square[2]
        exit(1)

    def find_3x3(square):
        for i in range(2):
            for j in range(4):
                if square in book[1]:
                    return book[1][square]
                square = square[2] + square[5] + square[8] + \
                         square[1] + square[4] + square[7] + \
                         square[0] + square[3] + square[6]

            square = square[2] + square[1] + square[0] + \
                     square[5] + square[4] + square[3] + \
                     square[8] + square[7] + square[6]
        exit(1)

    for _ in range(iters):
        if len(grid) % 2 == 0:
            for i in range(len(grid)):
                if i % 2 == 0:
                    new_grid.append("")
                    new_grid.append("")
                    new_grid.append("")
                for j in range(len(grid[i])):
                    if i % 2 == 0:
                        if j % 2 == 0:
                            new_square = find_2x2(grid[i][j:j+2] + \
                                                  grid[i+1][j:j+2])
                            new_grid[-3] += new_square[:3]
                            new_grid[-2] += new_square[3:6]
                            new_grid[-1] += new_square[6:]
        elif len(grid) % 3 == 0:
            for i in range(len(grid)):
                if i % 3 == 0:
                    new_grid.append("")
                    new_grid.append("")
                    new_grid.append("")
                    new_grid.append("")
                for j in range(len(grid[i])):
                    if i % 3 == 0:
                        if j % 3 == 0:
                            new_square = find_3x3(grid[i][j:j+3]   + \
                                                  grid[i+1][j:j+3] + \
                                                  grid[i+2][j:j+3])
                            new_grid[-4] += new_square[:4]
                            new_grid[-3] += new_square[4:8]
                            new_grid[-2] += new_square[8:12]
                            new_grid[-1] += new_square[12:]
        grid = new_grid
        new_grid = []
    return "".join(grid).count("#")

def main():
    puzzle_input = util.read.as_lines()

    pixels = solve(puzzle_input)

    print("The number of pixels on after 5 iterations is " + str(pixels) + ".")

class AOC_Tests(unittest.TestCase):
    def test_ex1(self):
        self.assertEqual(solve(["../.# => ##./#../...",
                                ".#./..#/### => #..#/..../..../#..#"], 2), 12)

run(main)
