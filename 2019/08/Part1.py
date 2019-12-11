#!/usr/bin/env python3

#Advent of Code
#2019 Day 8, Part 1
#Solution by James C. (https://github.com/JamesMCo)

import os, sys
sys.path.append(os.path.abspath("../.."))
import unittest, util.read
from util.tests import run

def solve(puzzle_input):
    def parse_layer(data, width, height):
        return data[:width*height], data[width*height:]

    layers = []
    while len(puzzle_input) > 0:
        l, puzzle_input = parse_layer(puzzle_input, 25, 6)
        layers.append(l)
    layers.sort(key=lambda x: x.count("0"))

    return layers[0].count("1") * layers[0].count("2")

def main():
    puzzle_input = util.read.as_string()

    ones_by_twos = solve(puzzle_input)

    print("The the number of 1 digits multiplied by the number of 2 digits is " + str(ones_by_twos) + ".")

class AOC_Tests(unittest.TestCase):
    @unittest.skip("No test cases")
    def test_ex1(self):
        pass

run(main)
