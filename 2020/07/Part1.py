#!/usr/bin/env python3

#Advent of Code
#2020 Day 7, Part 1
#Solution by James C. (https://github.com/JamesMCo)

import os, sys
sys.path.append(os.path.abspath("../.."))
import unittest, util.read
from util.tests import run

import re

def solve(puzzle_input):
    parent_name = re.compile(r"([\w ]+?) bags")
    children    = re.compile(r"(\d+) ([\w ]+) bags?")

    colour_rules = {}
    for colour in puzzle_input:
        if "no other bags" in colour:
            colour_rules[re.match(parent_name, colour).group(1)] = []
        else:
            colour_rules[re.match(parent_name, colour).group(1)] = re.findall(children, colour)

    found = 0
    just_found = set(["shiny gold"])
    while just_found:
        just_found_prev = just_found.copy()
        just_found = set()

        for current in list(colour_rules.keys()):
            if any(child[1] in just_found_prev for child in colour_rules[current]):
                found += 1
                just_found.add(current)
                del colour_rules[current]
    return found

def main():
    puzzle_input = util.read.as_lines()

    colours = solve(puzzle_input)

    print("The number of bag colours that can eventually contain at least one shiny gold bag is " + str(colours) + ".")

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
                                       "dotted black bags contain no other bags."]), 4)

if __name__ == "__main__":
    run(main)
