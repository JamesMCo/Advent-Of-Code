#!/usr/bin/env python3

#Advent of Code
#2019 Day 10, Part 2
#Solution by James C. (https://github.com/JamesMCo)

import os, sys
sys.path.append(os.path.abspath("../.."))
import unittest, util.read
from util.tests import run

from fractions import Fraction
from math import atan2

def solve(puzzle_input):
    width  = len(puzzle_input[0])
    height = len(puzzle_input)

    asteroids = [(x, y) for x in range(width) for y in range(height) if puzzle_input[y][x] == "#"]
    detections = {}
    gradients = set()

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
                gradients.add((dx, dy))

                a, b = x + dx, y + dy
                while (0 <= a < width) and (0 <= b < height):
                    if puzzle_input[b][a] == "#":
                        if (a, b) == (tx, ty):
                            detections[(x, y)] = detections[(x, y)] + 1
                        break
                    a += dx
                    b += dy

    laser_x, laser_y = sorted(detections.keys(), key=lambda z: detections[z])[-1]

    def find_angle(coords):
        dx, dy = coords
        grad = atan2(dy, dx)
        if dx >= 0 and dy < 0:
            pass
        elif dx >= 0 and dy >= 0:
            grad += 10
        elif dx < 0 and dy >= 0:
            grad += 20
        else:
            grad += 30
        return grad
    gradients = sorted(gradients, key=find_angle)

    vaporised = 0
    while True:
        for dx, dy in gradients:
            x, y = laser_x + dx, laser_y + dy
            
            while (0 <= x < width) and (0 <= y < height):
                if puzzle_input[y][x] == "#":
                    puzzle_input[y] = puzzle_input[y][:x] + "." + puzzle_input[y][x+1:]
                    vaporised += 1
                    break
                x += dx
                y += dy

            if vaporised == 200:
                return (x * 100) + y

def main():
    puzzle_input = util.read.as_lines()

    value = solve(puzzle_input)

    print("The value x * 100 + y of the 200th asteroid to be vaporised is " + str(value) + ".")

class AOC_Tests(unittest.TestCase):
    def test_ex1(self):
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
                                802)

if __name__ == "__main__":
    run(main)
