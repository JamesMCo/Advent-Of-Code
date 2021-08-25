#!/usr/bin/env python3

#Advent of Code
#2015 Day 9, Part 1
#Solution by James C. (https://github.com/JamesMCo)

import os, sys
sys.path.append(os.path.abspath("../.."))
import unittest, util.read
from util.tests import run
from itertools import permutations

def solve(puzzle_input):
    places = []
    distances = {}

    for line in puzzle_input:
        line = line.strip().split()
        for place in [line[0], line[2]]:
            if place not in places:
                places.append(place)
        distances[str(sorted([line[0], line[2]]))] = int(line[4])

    lowest = sum(distances.values())
    for route in permutations(places):
        running = 0
        for a, b in zip(route[:-1], route[1:]):
            running += distances[str(sorted([a, b]))]
        if running < lowest:
            lowest = running

    return lowest

def main():
    puzzle_input = util.read.as_lines()

    lowest = solve(puzzle_input)

    print("The distance of the shortest route is " + str(lowest) + ".")

class AOC_Tests(unittest.TestCase):
    def test_ex1(self):
        return self.assertEqual(solve(["London to Dublin = 464",
                                       "London to Belfast = 518",
                                       "Dublin to Belfast = 141"]), 605)

run(main)
