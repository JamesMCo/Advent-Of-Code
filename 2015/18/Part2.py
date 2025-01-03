#!/usr/bin/env python3

#Advent of Code
#2015 Day 18, Part 2
#Solution by James C. (https://github.com/JamesMCo)

import os, sys
sys.path.append(os.path.abspath("../.."))
import unittest, util.read
from util.tests import run

def solve(puzzle_input, steps=100):
    current = puzzle_input
    working = []

    current[0] = "#" + current[0][1:-1] + "#"
    current[-1] = "#" + current[-1][1:-1] + "#"

    def count_surrounding(x, y, current):
        c = 0
        l = len(current[0]) - 1

        if (x, y) in [(0, 0), (0, l), (l, 0), (l, l)]:
            return 3

        if y > 0:
            if x > 0:
                c += int(current[y-1][x-1] == "#")
            c += int(current[y-1][x] == "#")
            if x < l:
                c += int(current[y-1][x+1] == "#")

        if x > 0:
            c += int(current[y][x-1] == "#")
        if x < l:
            c += int(current[y][x+1] == "#")

        if y < l:
            if x > 0:
                c += int(current[y+1][x-1] == "#")
            c += int(current[y+1][x] == "#")
            if x < l:
                c += int(current[y+1][x+1] == "#")

        return c

    for step in range(steps):
        for y, row in enumerate(current):
            working.append("")

            for x, col in enumerate(row):
                c = count_surrounding(x, y, current)
                if col == "#":
                    if c in [2, 3]:
                        working[-1] += "#"
                    else:
                        working[-1] += "."
                else:
                    if c == 3:
                        working[-1] += "#"
                    else:
                        working[-1] += "."   

        current = working[:]
        working = []

    return sum(x.count("#") for x in current)

def main():
    puzzle_input = util.read.as_string_list("\n")

    on = solve(puzzle_input)

    print("After 100 steps, the number of lights on is " + str(on) + ".")

class AOC_Tests(unittest.TestCase):
    def test_ex1(self):
        return self.assertEqual(solve(["##.#.#",
                                       "...##.",
                                       "#....#",
                                       "..#...",
                                       "#.#..#",
                                       "####.#"], 1), 18)

    def test_ex2(self):
        return self.assertEqual(solve(["##.#.#",
                                       "...##.",
                                       "#....#",
                                       "..#...",
                                       "#.#..#",
                                       "####.#"], 2), 18)

    def test_ex3(self):
        return self.assertEqual(solve(["##.#.#",
                                       "...##.",
                                       "#....#",
                                       "..#...",
                                       "#.#..#",
                                       "####.#"], 3), 18)

    def test_ex4(self):
        return self.assertEqual(solve(["##.#.#",
                                       "...##.",
                                       "#....#",
                                       "..#...",
                                       "#.#..#",
                                       "####.#"], 4), 14)

    def test_ex5(self):
        return self.assertEqual(solve(["##.#.#",
                                       "...##.",
                                       "#....#",
                                       "..#...",
                                       "#.#..#",
                                       "####.#"], 5), 17)

if __name__ == "__main__":
    run(main)
