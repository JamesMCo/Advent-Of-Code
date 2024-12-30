#!/usr/bin/env python3

#Advent of Code
#2020 Day 2, Part 2
#Solution by James C. (https://github.com/JamesMCo)

import os, sys
sys.path.append(os.path.abspath("../.."))
import unittest, util.read
from util.tests import run

import re

def solve(puzzle_input):
    pattern = re.compile(r"(\d+)-(\d+) (\w): (\w+)")

    def aux(entry):
        pos1, pos2, character, password = re.match(pattern, entry).groups()
        return (password[int(pos1) - 1] == character) ^ (password[int(pos2) - 1] == character)

    return sum(aux(entry) for entry in puzzle_input)

def main():
    puzzle_input = util.read.as_lines()

    passwords = solve(puzzle_input)

    print("The number of valid passwords is " + str(passwords) + ".")

class AOC_Tests(unittest.TestCase):
    def test_ex1(self):
        return self.assertEqual(solve(["1-3 a: abcde",
                                       "1-3 b: cdefg",
                                       "2-9 c: ccccccccc"]), 1)

if __name__ == "__main__":
    run(main)
