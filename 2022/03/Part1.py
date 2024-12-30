#!/usr/bin/env python3

#Advent of Code
#2022 Day 3, Part 1
#Solution by James C. (https://github.com/JamesMCo)

import os, sys
sys.path.append(os.path.abspath("../.."))
import unittest, util.read
from util.tests import run

from string import ascii_lowercase

def solve(puzzle_input):
    def find_dupe(rucksack):
        first  = rucksack[:int(len(rucksack)/2)]
        second = rucksack[int(len(rucksack)/2):]
        return list(set(first).intersection(second))[0]

    def priority(item):
        return ord(item) + (1 - ord("a") if item in ascii_lowercase else 27 - ord("A"))

    return sum(priority(find_dupe(rucksack)) for rucksack in puzzle_input)

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
                                       "CrZsJsPPZsGzwwsLwLmpwMDw"]), 157)

if __name__ == "__main__":
    run(main)
