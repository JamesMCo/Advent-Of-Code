#!/usr/bin/env python3

#Advent of Code
#2020 Day 3, Part 1
#Solution by James C. (https://github.com/JamesMCo)

import os, sys
sys.path.append(os.path.abspath("../.."))
import unittest, util.read
from util.tests import run

def solve(puzzle_input):
    width  = len(puzzle_input[0])
    height = len(puzzle_input)

    x = y = 0
    trees = 0
    
    while y < height:
        if puzzle_input[y][x % width] == "#":
            trees += 1
        x += 3
        y += 1

    return trees


def main():
    puzzle_input = util.read.as_lines()

    trees = solve(puzzle_input)

    print("The number of trees encountered is " + str(trees) + ".")

class AOC_Tests(unittest.TestCase):
    def test_ex1(self):
        return self.assertEqual(solve(["..##.......",
                                       "#...#...#..",
                                       ".#....#..#.",
                                       "..#.#...#.#",
                                       ".#...##..#.",
                                       "..#.##.....",
                                       ".#.#.#....#",
                                       ".#........#",
                                       "#.##...#...",
                                       "#...##....#",
                                       ".#..#...#.#"]), 7)

run(main)
