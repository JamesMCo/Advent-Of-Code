#!/usr/bin/env python3

#Advent of Code
#2024 Day 5, Part 1
#Solution by James C. (https://github.com/JamesMCo)

import os, sys
sys.path.append(os.path.abspath("../.."))
import unittest, util.read
from util.tests import run

from collections import defaultdict

def solve(puzzle_input: list[str]) -> int:
    rules: dict[int, set[int]] = defaultdict(set)

    def is_ordered(head: int, tail: list[int]) -> bool:
        if not tail:
            # An update of just one page is in order
            return True
        elif any(head in rules[t] for t in tail):
            # If head is in rules[t], head is meant to come after t, so this is not ordered
            return False
        return is_ordered(tail[0], tail[1:])

    reading_rules: bool = True
    total: int = 0

    for line in puzzle_input:
        if reading_rules:
            if line == "":
                reading_rules = False
                continue
            before, after = map(int, line.split("|"))
            rules[before].add(after)

        else:
            update: list[int] = list(map(int, line.split(",")))
            if is_ordered(update[0], update[1:]):
                total += update[int(len(update)/2)]

    return total

def main() -> tuple[str, int]:
    puzzle_input = util.read.as_lines()

    return "The sum of the middle page numbers in correctly ordered updates is {}.", solve(puzzle_input)

class AOC_Tests(unittest.TestCase):
    def test_ex1(self):
        return self.assertEqual(solve(["47|53",
                                       "97|13",
                                       "97|61",
                                       "97|47",
                                       "75|29",
                                       "61|13",
                                       "75|53",
                                       "29|13",
                                       "97|29",
                                       "53|29",
                                       "61|53",
                                       "97|53",
                                       "61|29",
                                       "47|13",
                                       "75|47",
                                       "97|75",
                                       "47|61",
                                       "75|61",
                                       "47|29",
                                       "75|13",
                                       "53|13",
                                       "",
                                       "75,47,61,53,29",
                                       "97,61,53,29,13",
                                       "75,29,13",
                                       "75,97,47,61,53",
                                       "61,13,29",
                                       "97,13,75,29,47"]), 143)

if __name__ == "__main__":
    run(main)
