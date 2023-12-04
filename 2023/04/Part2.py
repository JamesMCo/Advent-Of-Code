#!/usr/bin/env python3

#Advent of Code
#2023 Day 4, Part 2
#Solution by James C. (https://github.com/JamesMCo)

import os, sys
sys.path.append(os.path.abspath("../.."))
import unittest, util.read
from util.tests import run

import re

def solve(puzzle_input):
    full_pattern: re.Pattern = re.compile(r"(.*):(.*)\|(.*)")
    card_num: re.Pattern = re.compile(r"Card ( *\d+)")
    numbers: re.Pattern = re.compile(r" ([ \d]\d)")

    cards = {n: 1 for n in range(1, len(puzzle_input) + 1)}

    def process_card(card_description: str):
        parts = full_pattern.match(card_description).groups()
        current_card = int(card_num.match(parts[0]).groups()[0])
        winning_numbers  = set(numbers.findall(parts[1]))
        numbers_you_have = set(numbers.findall(parts[2]))

        matches = len(winning_numbers & numbers_you_have)
        for next_card in range(current_card + 1, current_card + 1 + matches):
            cards[next_card] += cards[current_card]

    for card in puzzle_input:
        process_card(card)

    return sum(cards.values())

def main():
    puzzle_input = util.read.as_lines()

    return "The total number of scratchcards you end up with is {}.", solve(puzzle_input)

class AOC_Tests(unittest.TestCase):
    def test_ex1(self):
        return self.assertEqual(solve(["Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53",
                                       "Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19",
                                       "Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1",
                                       "Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83",
                                       "Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36",
                                       "Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11"]), 30)

run(main)
