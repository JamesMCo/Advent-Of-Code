#!/usr/bin/env python3

#Advent of Code
#2023 Day 4, Part 1
#Solution by James C. (https://github.com/JamesMCo)

import os, sys
sys.path.append(os.path.abspath("../.."))
import unittest, util.read
from util.tests import run

import re

def solve(puzzle_input):
    full_pattern: re.Pattern = re.compile(r"(.*):(.*)\|(.*)")
    numbers: re.Pattern = re.compile(r" ([ \d]\d)")

    def score_card(card_description: str) -> int:
        parts = full_pattern.match(card_description).groups()
        winning_numbers  = set(numbers.findall(parts[1]))
        numbers_you_have = set(numbers.findall(parts[2]))

        match len(winning_numbers & numbers_you_have):
            case 0: return 0
            case 1: return 1
            case n: return 2 ** (n-1)

    return sum(map(score_card, puzzle_input))

def main():
    puzzle_input = util.read.as_lines()

    return "The pile of scratchcards is worth {} points.", solve(puzzle_input)

class AOC_Tests(unittest.TestCase):
    def test_ex1(self):
        return self.assertEqual(solve(["Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53",
                                       "Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19",
                                       "Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1",
                                       "Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83",
                                       "Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36",
                                       "Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11"]), 13)

run(main)
