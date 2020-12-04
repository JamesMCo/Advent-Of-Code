#!/usr/bin/env python3

#Advent of Code
#2020 Day 3, Part 2
#Solution by James C. (https://github.com/JamesMCo)

import os, sys
sys.path.append(os.path.abspath("../.."))
import unittest, util.read
from util.tests import run

from math import prod

def solve(puzzle_input):
    width  = len(puzzle_input[0])
    height = len(puzzle_input)

    def aux(slope):
      x = y = 0
      trees = 0

      while y < height:
          if puzzle_input[y][x % width] == "#":
              trees += 1
          x += slope[0]
          y += slope[1]

      return trees

    return prod(aux(slope) for slope in [(1, 1), (3, 1), (5, 1), (7, 1), (1, 2)])

def main():
    puzzle_input = util.read.as_lines()

    trees = solve(puzzle_input)

    print("The product of the number of trees encountered on the listed slopes is " + str(trees) + ".")

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
                                       ".#..#...#.#"]), 336)

run(main)
