#!/usr/bin/env python3

#Advent of Code
#2018 Day 11, Part 2
#Solution by James C. (https://github.com/JamesMCo)

import os, sys
sys.path.append(os.path.abspath("../.."))
import unittest, util.read
from util.tests import run

def solve(puzzle_input):
    def get_power(x, y, d):
        if f"{x},{y}" in d:
            return d[f"{x},{y}"]
        
        rackID = x + 10
        power_level = rackID * y
        power_level += puzzle_input
        power_level *= rackID
        power_level = int((power_level % 1000) / 100)
        power_level -= 5
        d[f"{x},{y}"] = power_level
        
        return power_level
    

    grid            = {}
    max_power       = 0
    max_power_coord = "0,0,0"

    for x in range(1, 301):
        for y in range(1, 301):
            bound = min(300 - x, 300 - y)
            for size in range(1, bound+1):
                power = sum(get_power(X, Y, grid) for X in range(x, x+size) for Y in range(y, y+size))
                if power > max_power:
                    max_power       = power
                    max_power_coord = f"{x},{y},{size}"
                elif power < -5:
                    break

    return max_power_coord


def main():
    puzzle_input = util.read.as_int()

    coord = solve(puzzle_input)

    print("The X,Y,size identifier of the square with the largest total power is " + str(coord) + ".")

class AOC_Tests(unittest.TestCase):
    def test_ex1(self):
        self.assertEqual(solve(18), "90,269,16")

    def test_ex2(self):
        self.assertEqual(solve(42), "232,251,12")

if __name__ == "__main__":
    run(main)
