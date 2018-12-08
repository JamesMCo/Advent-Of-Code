#!/usr/bin/env python3

#Advent of Code
#2016 Day 7, Part 2
#Solution by James C. (https://github.com/JamesMCo)

import os, sys
sys.path.append(os.path.abspath("../.."))
import unittest, util.read
from util.tests import run

def solve(puzzle_input):
    supported = 0

    for line in puzzle_input:
        brackets = 0
        aba = []
        bab = []
        for i in range(len(line) - 2):
            if line[i] == "[":
                brackets += 1
            elif line[i] == "]":
                brackets -= 1
            elif brackets == 0 and line[i] != line[i+1] and line[i] == line[i+2]:
                if line[i] + line[i+1] + line[i+2] not in aba:
                    aba.append(line[i] + line[i+1] + line[i+2])
            elif brackets > 0 and line[i] != line[i+1] and line[i] == line[i+2]:
                if line[i] + line[i+1] + line[i+2] not in bab:
                    bab.append(line[i] + line[i+1] + line[i+2])
        for i in aba:
            if i[1] + i[0] + i[1] in bab:
                supported += 1
                break

    return supported

def main():
    puzzle_input = util.read.as_lines()

    supported = solve(puzzle_input)

    print("The number of SSL supporting IPs is " + str(supported) + ".")

class AOC_Tests(unittest.TestCase):
    def test_ex1(self):
        self.assertEqual(solve(["aba[bab]xyz"]), 1)

    def test_ex2(self):
        self.assertEqual(solve(["xyx[xyx]xyx"]), 0)

    def test_ex3(self):
        self.assertEqual(solve(["aaa[kek]eke"]), 1)

    def test_ex4(self):
        self.assertEqual(solve(["zazbz[bzb]cdb"]), 1)

run(main)
