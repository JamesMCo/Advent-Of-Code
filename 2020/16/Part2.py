#!/usr/bin/env python3

#Advent of Code
#2020 Day 16, Part 2
#Solution by James C. (https://github.com/JamesMCo)

import os, sys
sys.path.append(os.path.abspath("../.."))
import unittest, util.read
from util.tests import run

from math import prod
import re

def solve(puzzle_input):
    field_rule = re.compile("(\d+)-(\d+) or (\d+)-(\d+)")

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

    def is_invalid(l):
        return any(True for x in l if not any(r[0] <= x <= r[1] for f in fields.values() for r in f))

    fields         = {line.split(":")[0]:parse_rules(line) for line in consume_section()}
    your_ticket    = [int(n) for n in consume_section()[1].split(",")]
    nearby_tickets = [[int(n) for n in l.split(",")] for l in consume_section()[1:] if not is_invalid([int(n) for n in l.split(",")])]

    unallocated_fields = {k:set(n for n in range(len(fields))) for k in fields}
    allocated_fields   = {}
    while len(unallocated_fields) > 0:
        field_for_deletion = []
        for field in unallocated_fields:
            for col in list(unallocated_fields[field]):
                working = [t[col] for t in nearby_tickets]
                if not all(fields[field][0][0] <= t <= fields[field][0][1] or fields[field][1][0] <= t <= fields[field][1][1] for t in working):
                    unallocated_fields[field].remove(col)

            if len(unallocated_fields[field]) == 1:
                (allocated_fields[field],) = unallocated_fields[field]
                for other in unallocated_fields:
                    unallocated_fields[other].discard(allocated_fields[field])
                field_for_deletion.append(field)
        for d in field_for_deletion:
            del unallocated_fields[d]

    return prod(your_ticket[allocated_fields[field]] for field in allocated_fields if field.startswith("departure"))

def main():
    puzzle_input = util.read.as_lines()

    product = solve(puzzle_input)

    print("The product of the six values starting with the word departure is " + str(product) + ".")

class AOC_Tests(unittest.TestCase):
    @unittest.skip("No test cases")
    def test_ex1(self):
        pass

run(main)
