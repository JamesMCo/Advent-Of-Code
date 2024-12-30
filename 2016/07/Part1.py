#!/usr/bin/env python3

#Advent of Code
#2016 Day 7, Part 1
#Solution by James C. (https://github.com/JamesMCo)

import os, sys
sys.path.append(os.path.abspath("../.."))
import unittest, util.read
from util.tests import run

def solve(puzzle_input):
    supported = 0

    for line in puzzle_input:
        brackets = 0
        this_sup = False
        invalid  = False
        for i in range(len(line) - 3):
            if line[i] == "[":
                brackets += 1
            elif line[i] == "]":
                brackets -= 1
            elif brackets == 0 and line[i] != line[i+1] and line[i] + line[i+1] == line[i+3] + line[i+2]:
                this_sup = True
            elif brackets > 0 and line[i] != line[i+1] and line[i] + line[i+1] == line[i+3] + line[i+2]:
                invalid = True
        if not invalid:
            supported += this_sup

    return supported

def main():
    puzzle_input = util.read.as_lines()

    supported = solve(puzzle_input)

    print("The number of TLS supporting IPs is " + str(supported) + ".")

class AOC_Tests(unittest.TestCase):
    def test_ex1(self):
        self.assertEqual(solve(["abba[mnop]qrst"]), 1)

    def test_ex2(self):
        self.assertEqual(solve(["abcd[bddb]xyyx"]), 0)

    def test_ex3(self):
        self.assertEqual(solve(["aaaa[qwer]tyui"]), 0)

    def test_ex4(self):
        self.assertEqual(solve(["ioxxoj[asdfgh]zxcvbn"]), 1)

if __name__ == "__main__":
    run(main)
