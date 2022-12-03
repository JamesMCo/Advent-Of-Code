#!/usr/bin/env python3

#Advent of Code
#2022 Day 3, Part 2
#Solution by James C. (https://github.com/JamesMCo)

import os, sys
sys.path.append(os.path.abspath("../.."))
import unittest, util.read
from util.tests import run

from string import ascii_lowercase

def solve(puzzle_input):
    def find_dupe(first, second, third):
        return list(set(first).intersection(second).intersection(third))[0]

    def priority(item):
        return ord(item) + (1 - ord("a") if item in ascii_lowercase else 27 - ord("A"))

    return sum(priority(find_dupe(*puzzle_input[i:i+3])) for i in range(0, len(puzzle_input), 3))

def main():
    puzzle_input = util.read.as_lines()

    priorities = solve(puzzle_input)

    print("The sum of the priorities is " + str(priorities) + ".")

class AOC_Tests(unittest.TestCase):
    def test_ex1(self):
        return self.assertEqual(solve(["vJrwpWtwJgWrhcsFMMfFFhFp",
                                       "jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL",
                                       "PmmdzqPrVvPwwTWBwg",
                                       "wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn",
                                       "ttgJtRGJQctTZtZT",
                                       "CrZsJsPPZsGzwwsLwLmpwMDw"]), 70)

run(main)
