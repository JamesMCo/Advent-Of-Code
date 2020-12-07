#!/usr/bin/env python3

#Advent of Code
#2020 Day 7, Part 2
#Solution by James C. (https://github.com/JamesMCo)

import os, sys
sys.path.append(os.path.abspath("../.."))
import unittest, util.read
from util.tests import run

import collections, re

def solve(puzzle_input):
    parent_name = re.compile("([\w ]+?) bags")
    children    = re.compile("(\d+) ([\w ]+) bags?")

    colour_rules = {}
    for colour in puzzle_input:
        if "no other bags" in colour:
            colour_rules[re.match(parent_name, colour).group(1)] = []
        else:
            colour_rules[re.match(parent_name, colour).group(1)] = re.findall(children, colour)

    processing = collections.deque(["shiny gold"])
    processed  = -1
    while processing:
        current = processing.popleft()
        for amount, colour in colour_rules[current]:
            processing += [colour] * int(amount)
        processed += 1

    return processed

def main():
    puzzle_input = util.read.as_lines()

    colours = solve(puzzle_input)

    print("The number of individual bags required inside a single shiny gold bag is " + str(colours) + ".")

class AOC_Tests(unittest.TestCase):
    def test_ex1(self):
        return self.assertEqual(solve(["light red bags contain 1 bright white bag, 2 muted yellow bags.",
                                       "dark orange bags contain 3 bright white bags, 4 muted yellow bags.",
                                       "bright white bags contain 1 shiny gold bag.",
                                       "muted yellow bags contain 2 shiny gold bags, 9 faded blue bags.",
                                       "shiny gold bags contain 1 dark olive bag, 2 vibrant plum bags.",
                                       "dark olive bags contain 3 faded blue bags, 4 dotted black bags.",
                                       "vibrant plum bags contain 5 faded blue bags, 6 dotted black bags.",
                                       "faded blue bags contain no other bags.",
                                       "dotted black bags contain no other bags."]), 32)

    def test_ex2(self):
        return self.assertEqual(solve(["shiny gold bags contain 2 dark red bags.",
                                       "dark red bags contain 2 dark orange bags.",
                                       "dark orange bags contain 2 dark yellow bags.",
                                       "dark yellow bags contain 2 dark green bags.",
                                       "dark green bags contain 2 dark blue bags.",
                                       "dark blue bags contain 2 dark violet bags.",
                                       "dark violet bags contain no other bags."]), 126)

run(main)
