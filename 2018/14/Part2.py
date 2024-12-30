#!/usr/bin/env python3

#Advent of Code
#2018 Day 14, Part 2
#Solution by James C. (https://github.com/JamesMCo)

import os, sys
sys.path.append(os.path.abspath("../.."))
import unittest, util.read
from util.tests import run

def solve(puzzle_input):
    scores = [3, 7]
    elf1 = 0
    elf2 = 1
    latest = "0"*(len(puzzle_input) + 1)
    latest = latest[2:] + "37"

    while puzzle_input not in latest:
        if scores[elf1] + scores[elf2] < 10:
            scores.append(scores[elf1] + scores[elf2])
            latest = latest[1:] + str(scores[elf1] + scores[elf2])
        else:
            scores.append(int(str(scores[elf1] + scores[elf2])[0]))
            scores.append(int(str(scores[elf1] + scores[elf2])[1]))

            latest = latest[2:] + str(scores[elf1] + scores[elf2])

        elf1 = (elf1 + 1 + scores[elf1]) % len(scores)
        elf2 = (elf2 + 1 + scores[elf2]) % len(scores)

    return "".join(str(x) for x in scores).index(puzzle_input)

def main():
    puzzle_input = util.read.as_string()

    number_of_scores = solve(puzzle_input)

    print("The number of recipes to the left of the score sequences is " + str(number_of_scores) + ".")

class AOC_Tests(unittest.TestCase):
    def test_ex1(self):
        self.assertEqual(solve("51589"), 9)

    def test_ex2(self):
        self.assertEqual(solve("01245"), 5)

    def test_ex3(self):
        self.assertEqual(solve("92510"), 18)

    def test_ex4(self):
        self.assertEqual(solve("59414"), 2018)

if __name__ == "__main__":
    run(main)
