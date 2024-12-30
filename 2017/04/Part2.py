#!/usr/bin/env python3

#Advent of Code
#2017 Day 4, Part 2
#Solution by James C. (https://github.com/JamesMCo)

import os, sys
sys.path.append(os.path.abspath("../.."))
import unittest, util.read
from util.tests import run

from itertools import permutations

def solve(puzzle_input):
    count = 0

    for passphrase in puzzle_input:
        words = passphrase.split(" ")
        if sorted(words) == sorted(set(words)):
            invalid = False
            for i in words:
                for perm in permutations(i):
                    if "".join(perm) != i and "".join(perm) in words:
                        invalid = True
                        break
                if invalid:
                    break
            if not invalid:
                count += 1

    return count

def main():
    puzzle_input = util.read.as_lines()

    count = solve(puzzle_input)

    print("The number of valid passphrases is " + str(count) + ".")

class AOC_Tests(unittest.TestCase):
    def test_ex1(self):
        self.assertEqual(solve(["abcde fghij", "abcde xyz ecdab", "a ab abc abd abf abj", "iiii oiii ooii oooi oooo", "oiii ioii iioi iiio"]), 3)

if __name__ == "__main__":
    run(main)
