#!/usr/bin/env python3

#Advent of Code
#2018 Day 14, Part 1
#Solution by James C. (https://github.com/JamesMCo)

import os, sys
sys.path.append(os.path.abspath("../.."))
import unittest, util.read
from util.tests import run

def solve(puzzle_input):
    scores = [3, 7]
    elf1 = 0
    elf2 = 1
    while len(scores) < puzzle_input + 10:
        if scores[elf1] + scores[elf2] < 10:
            scores.append(scores[elf1] + scores[elf2])
        else:
            scores.append(int(str(scores[elf1] + scores[elf2])[0]))
            scores.append(int(str(scores[elf1] + scores[elf2])[1]))

        elf1 = (elf1 + 1 + scores[elf1]) % len(scores)
        elf2 = (elf2 + 1 + scores[elf2]) % len(scores)

    return "".join(str(x) for x in scores[puzzle_input:puzzle_input+10])

def main():
    puzzle_input = util.read.as_int()

    scores = solve(puzzle_input)

    print("The scores of the ten recipes are " + str(scores) + ".")

class AOC_Tests(unittest.TestCase):
    def test_ex1(self):
        self.assertEqual(solve(9), "5158916779")

    def test_ex2(self):
        self.assertEqual(solve(5), "0124515891")

    def test_ex3(self):
        self.assertEqual(solve(18), "9251071085")

    def test_ex4(self):
        self.assertEqual(solve(2018), "5941429882")

run(main)
