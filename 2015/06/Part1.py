#!/usr/bin/env python3

#Advent of Code
#2015 Day 6, Part 1
#Solution by James C. (https://github.com/JamesMCo)

import os, sys
sys.path.append(os.path.abspath("../.."))
import unittest, util.read
from util.tests import run

def solve(puzzle_input):
    lights = [[0 for i in range(1000)] for i in range(1000)]
    on = 0

    for i in puzzle_input:
        if i.split(" ")[0:2] in [["turn", "off"], ["turn", "on"]]:
            for x in range(int(i.split(" ")[2].split(",")[0]), int(i.split(" ")[4].split(",")[0])+1):
                for y in range(int(i.split(" ")[2].split(",")[1]), int(i.split(" ")[4].split(",")[1])+1):
                    if i.split(" ")[1] == "on":
                        lights[x][y] = 1
                    else:
                        lights[x][y] = 0
        elif i.split(" ")[0] == "toggle":
            for x in range(int(i.split(" ")[1].split(",")[0]), int(i.split(" ")[3].split(",")[0])+1):
                for y in range(int(i.split(" ")[1].split(",")[1]), int(i.split(" ")[3].split(",")[1])+1):
                    if lights[x][y] == 0:
                        lights[x][y] = 1
                    else:
                        lights[x][y] = 0
        else:
            print("Problem!")

    for x in lights:
        for y in x:
            if y == 1:
                on += 1

    return on

def main():
    puzzle_input = util.read.as_lines()

    on = solve(puzzle_input)

    print("The number of lights that are lit is " + str(on) + ".")

class AOC_Tests(unittest.TestCase):
    def test_ex1(self):
        return self.assertEqual(solve(["turn on 0,0 through 999,999"]), 1000000)

    def test_ex2(self):
        return self.assertEqual(solve(["toggle 0,0 through 999,0"]), 1000)

    def test_ex3(self):
        return self.assertEqual(solve(["turn off 499,499 through 500,500"]), 0)

run(main)
