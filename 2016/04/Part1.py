#!/usr/bin/env python3

#Advent of Code
#2016 Day 4, Part 1
#Solution by James C. (https://github.com/JamesMCo)

import os, sys
sys.path.append(os.path.abspath("../.."))
import unittest, util.read
from util.tests import run

from collections import Counter

def solve(puzzle_input):
    sector_ids = 0

    def getchecksum(s):
        c = Counter(s)
        d = {}
        for l in c:
            if c[l] in d:
                d[c[l]] += l
            else:
                d[c[l]] = l
        f = ""
        for i in sorted(d, reverse=True):
            f += "".join(sorted(list(d[i])))
        return f[:5]

    for room in puzzle_input:
        if room == "": continue
        working = "".join(sorted(room.split("-")[:-1]))
        if getchecksum(working) == room.split("[")[1][:-1]:
            sector_ids += int(room.split("-")[-1][:3])

    return sector_ids

def main():
    puzzle_input = util.read.as_lines()

    sector_ids = solve(puzzle_input)

    print("The sum of the sector IDs is " + str(sector_ids) + ".")

class AOC_Tests(unittest.TestCase):
    def test_ex1(self):
        self.assertEqual(solve(["aaaaa-bbb-z-y-x-123[abxyz]",
                                "a-b-c-d-e-f-g-h-987[abcde]",
                                "not-a-real-room-404[oarel]",
                                "totally-real-room-200[decoy]"]), 1514)

run(main)
