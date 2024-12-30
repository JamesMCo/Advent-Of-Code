#!/usr/bin/env python3

#Advent of Code
#2017 Day 13, Part 2
#Solution by James C. (https://github.com/JamesMCo)

import os, sys
sys.path.append(os.path.abspath("../.."))
import unittest, util.read
from util.tests import run

def calc_severity(layers, delay):
    caught = 0
    step = 0
    final = max(layers)
    
    while step <= final:
        if step in layers:
            if (step + delay) % ((layers[step] - 1) * 2) == 0:
                caught = 1
        step += 1

    return caught


def solve(puzzle_input):
    layers = {}
    for l in puzzle_input:
        layers[int(l.split(": ")[0])] = int(l.split(": ")[1])
    delay = 0

    while calc_severity(layers, delay) != 0:
        delay += 1

    return delay

def main():
    puzzle_input = util.read.as_lines()

    picoseconds = solve(puzzle_input)

    print("The fewest number of picoseconds to delay the packet by to avoid being caught is " + str(picoseconds) + ".")

class AOC_Tests(unittest.TestCase):
    def test_ex1(self):
        self.assertEqual(solve(["0: 3",
                                "1: 2",
                                "4: 4",
                                "6: 4"]), 10)

if __name__ == "__main__":
    run(main)
