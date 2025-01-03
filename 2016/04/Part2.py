#!/usr/bin/env python3

#Advent of Code
#2016 Day 4, Part 2
#Solution by James C. (https://github.com/JamesMCo)

import os, sys
sys.path.append(os.path.abspath("../.."))
import unittest, util.read
from util.tests import run

from collections import Counter

def solve(puzzle_input):
    valid = []

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

    def shift(s, k):
        k %= 26
        alpha = "abcdefghijklmnopqrstuvwxyz" * 2
        alpha += alpha.upper()
        def get_i():
            for i in range(26):
                yield i
            for i in range(53, 78):
                yield i
        ROT = {alpha[i]: alpha[i + k] for i in get_i()}
        return "".join(ROT.get(i, i) for i in s)

    for room in puzzle_input:
        if room == "": continue
        working = "".join(sorted(room.split("-")[:-1]))
        if getchecksum(working) == room.split("[")[1][:-1]:
            valid.append(room)

    for room in valid:
        cur = shift("-".join(sorted(room.split("-")[:-1])), int(room.split("-")[-1][:3]))
        if "north" in cur or "pole" in cur:
            return int(room.split("-")[3].split("[")[0])

def main():
    puzzle_input = util.read.as_lines()

    room = solve(puzzle_input)

    print("The room with the North Pole objects is " + str(room) + ".")

class AOC_Tests(unittest.TestCase):
    @unittest.skip("No test cases")
    def test_ex1(self):
        pass

if __name__ == "__main__":
    run(main)
