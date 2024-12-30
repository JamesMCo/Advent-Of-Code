#!/usr/bin/env python3

#Advent of Code
#2018 Day 22, Part 1
#Solution by James C. (https://github.com/JamesMCo)

import os, sys
sys.path.append(os.path.abspath("../.."))
import unittest, util.read
from util.tests import run

def solve(puzzle_input):
    depth = int(puzzle_input[0].split()[1])
    target_x, target_y = [int(x) for x in puzzle_input[1].split()[1].split(",")]
    
    g_indices = {}
    g_indices["0,0"] = 0
    g_indices[f"{target_x},{target_y}"] = 0


    def geologic_index(x, y):
        if f"{x},{y}" in g_indices:
            return g_indices[f"{x},{y}"]
        elif y == 0:
            g_indices[f"{x},{y}"] = x * 16807
            return g_indices[f"{x},{y}"]
        elif x == 0:
            g_indices[f"{x},{y}"] = y * 48271
            return g_indices[f"{x},{y}"]
        else:
            g_indices[f"{x},{y}"] = erosion_level(x-1, y) * erosion_level(x, y-1)
            return g_indices[f"{x},{y}"]

    def erosion_level(x, y):
        return (geologic_index(x, y) + depth) % 20183

    def coord_type(x, y):
        return ["rocky", "wet", "narrow"][erosion_level(x, y) % 3]

    def risk_level(x, y):
        return {"rocky": 0, "wet": 1, "narrow": 2}[coord_type(x, y)]


    return sum(risk_level(x, y) for x in range(0, target_x+1) for y in range(0, target_y+1))

def main():
    puzzle_input = util.read.as_lines()

    risk_level_sum = solve(puzzle_input)

    print("The total risk level for the smallest rectangle that includes 0,0 and the target is " + str(risk_level_sum) + ".")

class AOC_Tests(unittest.TestCase):
    def test_ex1(self):
        self.assertEqual(solve(["depth: 510",
                                "target: 10,10"]), 114)

if __name__ == "__main__":
    run(main)
