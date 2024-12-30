#!/usr/bin/env python3

#Advent of Code
#2021 Day 14, Part 2
#Solution by James C. (https://github.com/JamesMCo)

import os, sys
sys.path.append(os.path.abspath("../.."))
import unittest, util.read
from util.tests import run

from collections import Counter, defaultdict
from itertools import pairwise

def solve(puzzle_input):
    polymer = defaultdict(int)
    for pair in pairwise(puzzle_input[0]):
        polymer[pair] += 1

    rules = defaultdict(str)
    for rule in puzzle_input[2:]:
        rules[tuple(rule.split()[0])] = rule.split()[2]

    for i in range(1, 41):
        new_polymer = defaultdict(int)
        for pair in polymer:
            new_polymer[(pair[0], rules[pair])] += polymer[pair]
            new_polymer[(rules[pair], pair[1])] += polymer[pair]
        polymer = new_polymer.copy()

    quantities = defaultdict(int)
    # Force first and last elements to be double counted for later logic
    # (pairwise means first and last were only counted once, such as
    # [AB, BC, CD, DE] leading to A and E only being included once each)
    quantities[puzzle_input[0][0]]  += 1
    quantities[puzzle_input[0][-1]] += 1
    for pair in polymer:
        quantities[pair[0]] += polymer[pair]
        quantities[pair[1]] += polymer[pair]
    quantities = Counter(quantities).most_common()
    # All elements are double counted, so divide by 2 to get true counts
    return int((quantities[0][1] - quantities[-1][1])/2)

def main():
    puzzle_input = util.read.as_lines()

    elements = solve(puzzle_input)

    print("The quantity of the most common element minus the quantity of the least common element is " + str(elements) + ".")

class AOC_Tests(unittest.TestCase):
    def test_ex1(self):
        return self.assertEqual(solve(["NNCB",
                                       "",
                                       "CH -> B",
                                       "HH -> N",
                                       "CB -> H",
                                       "NH -> C",
                                       "HB -> C",
                                       "HC -> B",
                                       "HN -> C",
                                       "NN -> C",
                                       "BH -> H",
                                       "NC -> B",
                                       "NB -> B",
                                       "BN -> B",
                                       "BB -> N",
                                       "BC -> B",
                                       "CC -> N",
                                       "CN -> C"]), 2188189693529)

if __name__ == "__main__":
    run(main)
