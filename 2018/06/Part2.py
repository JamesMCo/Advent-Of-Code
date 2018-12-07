#!/usr/bin/env python3

#Advent of Code
#Day 6, Part 2
#Solution by James C. (https://github.com/JamesMCo)

import os, sys, colorama, time
sys.path.append(os.path.abspath("../.."))
import unittest
from util.tests import run

def solve(puzzle_input, max_sum=10_000):
    def distance(a, b):
        return abs(a[0]-b[0]) + abs(a[1]-b[1])

    puzzle_input = [(int(x.split(", ")[0]), int(x.split(", ")[1])) for x in puzzle_input]

    mid_x = int( ( min([z[0] for z in puzzle_input]) + max([z[0] for z in puzzle_input]) ) /2 )
    mid_y = int( ( min([z[1] for z in puzzle_input]) + max([z[1] for z in puzzle_input]) ) /2 )

    left_x = mid_x
    while sum([distance(z, (left_x, mid_y)) for z in puzzle_input]) < max_sum:
        left_x -= 1
    left_x -= 10

    right_x = mid_x
    while sum([distance(z, (right_x, mid_y)) for z in puzzle_input]) < max_sum:
        right_x += 1
    right_x += 10

    top_y = mid_y
    while sum([distance(z, (mid_x, top_y)) for z in puzzle_input]) < max_sum:
        top_y -= 1
    top_y -= 10

    bot_y = mid_y
    while sum([distance(z, (mid_x, bot_y)) for z in puzzle_input]) < max_sum:
        bot_y += 1
    bot_y += 10

    region = 0
    for x in range(left_x, right_x+1):
        for y in range(top_y, bot_y+1):
            working = [distance(z, (x, y)) for z in puzzle_input]
            if sum(working) < max_sum:
                region += 1

    return region

def main():
    f = open("puzzle_input.txt")
    puzzle_input = f.read().strip().split("\n")
    f.close()

    area = solve(puzzle_input)

    print("The size of the region is " + str(area) + ".")

class AOC_Tests(unittest.TestCase):
    def test_ex1(self):
        self.assertEqual(solve(["1, 1",
                                "1, 6",
                                "8, 3",
                                "3, 4",
                                "5, 5",
                                "8, 9"], 32), 16)

run(main)
