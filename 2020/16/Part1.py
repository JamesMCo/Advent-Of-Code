#!/usr/bin/env python3

#Advent of Code
#2020 Day 16, Part 1
#Solution by James C. (https://github.com/JamesMCo)

import os, sys
sys.path.append(os.path.abspath("../.."))
import unittest, util.read
from util.tests import run

import re

def solve(puzzle_input):
    field_rule = re.compile(r"(\d+)-(\d+) or (\d+)-(\d+)")

    def consume_section():
        output = []
        while puzzle_input:
            line = puzzle_input.pop(0)
            if line == "":
                break
            output.append(line)
        return output

    def parse_rules(l):
        vals = re.search(field_rule, l).groups()
        return ((int(vals[0]), int(vals[1])), (int(vals[2]), int(vals[3])))

    def find_invalid(l):
        return sum(x for x in [int(n) for n in l.split(",")] if not any(r[0] <= x <= r[1] for f in fields.values() for r in f))

    fields         = {line.split(":")[0]:parse_rules(line) for line in consume_section()}
    your_ticket    = consume_section()[1]
    nearby_tickets = consume_section()[1:]

    return sum(find_invalid(ticket) for ticket in nearby_tickets)

def main():
    puzzle_input = util.read.as_lines()

    error_rate = solve(puzzle_input)

    print("The ticket scanning error rate is " + str(error_rate) + ".")

class AOC_Tests(unittest.TestCase):
    def test_ex1(self):
        return self.assertEqual(solve(["class: 1-3 or 5-7",
                                       "row: 6-11 or 33-44",
                                       "seat: 13-40 or 45-50",
                                       "",
                                       "your ticket:",
                                       "7,1,14",
                                       "",
                                       "nearby tickets:",
                                       "7,3,47",
                                       "40,4,50",
                                       "55,2,20",
                                       "38,6,12"]), 71)

run(main)
