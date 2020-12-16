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
    # So far, this solution is able to determine all but 2 of the correct positions for the fields,
    # but is unable to find any valid options for the 2 remaining fields. To get the second star, I
    # found what the products would be under both options for the field orders, and tried to submit
    # both to the website (with the second attempt working). I plan to try to make part 2 work
    # fully later today.

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
        return sum(x for x in l if not any(r[0] <= x <= r[1] for f in fields.values() for r in f)) >= 1

    fields         = {line.split(":")[0]:parse_rules(line) for line in consume_section()}
    your_ticket    = [int(n) for n in consume_section()[1].split(",")]
    nearby_tickets = [[int(n) for n in l.split(",")] for l in consume_section()[1:] if not is_invalid([int(n) for n in l.split(",")])]
    # with open("debug.txt", "w") as f:
    #     f.write("\n".join(",".join(str(n) for n in l) for l in nearby_tickets))
    # return

    unallocated_fields = {k:set(n for n in range(len(fields))) for k in fields}
    allocated_fields   = {}
    while len(unallocated_fields) > 0:
        changed = False
        field_for_deletion = []
        for field in unallocated_fields:
            for col in list(unallocated_fields[field]):
                working = [t[col] for t in nearby_tickets]
                # print(f"Checking {working} against {fields[field]}")
                if not all(fields[field][0][0] <= t <= fields[field][0][1] or fields[field][1][0] <= t <= fields[field][1][1] for t in working):
                    if field == "price":
                        for i, t in enumerate(working):
                            if not (fields[field][0][0] <= t <= fields[field][0][1] or fields[field][1][0] <= t <= fields[field][1][1]):
                                print(f"{i}, {t}: {fields[field][0][0] <= t <= fields[field][0][1] or fields[field][1][0] <= t <= fields[field][1][1]}")
                    unallocated_fields[field].remove(col)
                    print(f"{col} is not a correct column for field {field}")
                    if len(unallocated_fields[field]) == 0:
                        input(f"{field} just removed its last possible col")
                    changed = True
            print(f"{field} potential matches = {unallocated_fields[field]}")

            if len(unallocated_fields[field]) == 1:
                print(f"This means {field} is known!")
                (allocated_fields[field],) = unallocated_fields[field]
                for other in unallocated_fields:
                    if other != field and allocated_fields[field] in unallocated_fields[other]:
                        unallocated_fields[other].remove(allocated_fields[field])
                field_for_deletion.append(field)
                changed = True
            print()
        for d in field_for_deletion:
            del unallocated_fields[d]

        if not changed:
        #     print("Nothing changed")
            print(allocated_fields)
            print(unallocated_fields)
            exit(1)
            # input()
        # input()
        # print(unallocated_fields)

    return prod(your_ticket[allocated_fields[field]] for field in allocated_fields if field.startswith("departure"))

def main():
    puzzle_input = util.read.as_lines()

    product = solve(puzzle_input)

    print("The product of the six values starting with the word departure is " + str(product) + ".")

class AOC_Tests(unittest.TestCase):
    # def test_ex1(self):
    #     return self.assertEqual(solve(["class: 0-1 or 4-19",
    #                                    "row: 0-5 or 8-19",
    #                                    "seat: 0-13 or 16-19",
    #                                    "",
    #                                    "your ticket:",
    #                                    "11,12,13",
    #                                    "",
    #                                    "nearby tickets:",
    #                                    "3,9,18",
    #                                    "15,1,5",
    #                                    "5,14,9"]), 0)
    @unittest.skip("No test cases")
    def test_ex1(self):
        pass

run(main)
