#!/usr/bin/env python3

#Advent of Code
#2021 Day 14, Part 1
#Solution by James C. (https://github.com/JamesMCo)

import os, sys
sys.path.append(os.path.abspath("../.."))
import unittest, util.read
from util.tests import run

from collections import Counter, defaultdict
from itertools import pairwise

def solve(puzzle_input):
    polymer = puzzle_input[0]

    rules = defaultdict(str)
    for rule in puzzle_input[2:]:
        rules[tuple(rule.split()[0])] = rule.split()[2]

    for i in range(1, 11):
        new_polymer = ""
        for pair in pairwise(polymer):
            new_polymer += pair[0] + rules[pair]
        polymer = new_polymer + polymer[-1]

    quantities = Counter(polymer).most_common()
    return quantities[0][1] - quantities[-1][1]

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
                                       "CN -> C"]), 1588)

run(main)
