#!/usr/bin/env python3

#Advent of Code
#2016 Day 6, Part 1
#Solution by James C. (https://github.com/JamesMCo)

import os, sys
sys.path.append(os.path.abspath("../.."))
import unittest, util.read
from util.tests import run

from collections import Counter

def solve(puzzle_input):
    message = ""

    for i in range(len(puzzle_input[0])):
        letters = [x[i] for x in puzzle_input]
        c = Counter(letters)
        message += c.most_common()[0][0]

    return message

def main():
    puzzle_input = util.read.as_lines()

    message = solve(puzzle_input)

    print("The message is " + message + ".")

class AOC_Tests(unittest.TestCase):
    def test_ex1(self):
        self.assertEqual(solve(["eedadn",
                                "drvtee",
                                "eandsr",
                                "raavrd",
                                "atevrs",
                                "tsrnev",
                                "sdttsa",
                                "rasrtv",
                                "nssdts",
                                "ntnada",
                                "svetve",
                                "tesnvt",
                                "vntsnd",
                                "vrdear",
                                "dvrsen",
                                "enarar"]), "easter")

run(main)
