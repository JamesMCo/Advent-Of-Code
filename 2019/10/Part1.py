#!/usr/bin/env python3

#Advent of Code
#2019 Day 10, Part 1
#Solution by James C. (https://github.com/JamesMCo)

import os, sys
sys.path.append(os.path.abspath("../.."))
import unittest, util.read
from util.tests import run

from fractions import Fraction

def solve(puzzle_input):
    width  = len(puzzle_input[0])
    height = len(puzzle_input)

    asteroids = [(x, y) for x in range(width) for y in range(height) if puzzle_input[y][x] == "#"]
    detections = {}

    for x in range(width):
        for y in range(height):
            if puzzle_input[y][x] == ".":
                continue

            detections[(x, y)] = 0
            for tx, ty in asteroids:
                if (x, y) == (tx, ty):
                    continue

                if x == tx:
                    dy, dx = 1, 0
                else:
                    f = Fraction(ty-y, tx-x)
                    dy, dx = abs(f.numerator), abs(f.denominator)
                if tx < x:
                    dx *= -1
                if ty < y:
                    dy *= -1

                a, b = x + dx, y + dy
                while (0 <= a < width) and (0 <= b < height):
                    if puzzle_input[b][a] == "#":
                        if (a, b) == (tx, ty):
                            detections[(x, y)] = detections[(x, y)] + 1
                        break
                    a += dx
                    b += dy

    return max(detections.values())

def main():
    puzzle_input = util.read.as_lines()

    asteroids = solve(puzzle_input)

    print("The number of other asteroids can be detected from the best location is " + str(asteroids) + ".")

class AOC_Tests(unittest.TestCase):
    def test_ex1(self):
        self.assertEqual(solve([".#..#",
                                ".....",
                                "#####",
                                "....#",
                                "...##"]),
                                8)

    def test_ex2(self):
        self.assertEqual(solve(["......#.#.",
                                "#..#.#....",
                                "..#######.",
                                ".#.#.###..",
                                ".#..#.....",
                                "..#....#.#",
                                "#..#....#.",
                                ".##.#..###",
                                "##...#..#.",
                                ".#....####"]),
                                33)

    def test_ex3(self):
        self.assertEqual(solve(["#.#...#.#.",
                                ".###....#.",
                                ".#....#...",
                                "##.#.#.#.#",
                                "....#.#.#.",
                                ".##..###.#",
                                "..#...##..",
                                "..##....##",
                                "......#...",
                                ".####.###."]),
                                35)

    def test_ex4(self):
        self.assertEqual(solve([".#..#..###",
                                "####.###.#",
                                "....###.#.",
                                "..###.##.#",
                                "##.##.#.#.",
                                "....###..#",
                                "..#.#..#.#",
                                "#..#.#.###",
                                ".##...##.#",
                                ".....#.#.."]),
                                41)

    def test_ex5(self):
        self.assertEqual(solve([".#..##.###...#######",
                                "##.############..##.",
                                ".#.######.########.#",
                                ".###.#######.####.#.",
                                "#####.##.#.##.###.##",
                                "..#####..#.#########",
                                "####################",
                                "#.####....###.#.#.##",
                                "##.#################",
                                "#####.##.###..####..",
                                "..######..##.#######",
                                "####.##.####...##..#",
                                ".#####..#.######.###",
                                "##...#.##########...",
                                "#.##########.#######",
                                ".####.#.###.###.#.##",
                                "....##.##.###..#####",
                                ".#.#.###########.###",
                                "#.#.#.#####.####.###",
                                "###.##.####.##.#..##"]),
                                210)

run(main)
