#!/usr/bin/env python3

#Advent of Code
#Day 4, Part 1
#Solution by James C. (https://github.com/JamesMCo)

import os, sys
sys.path.append(os.path.abspath("../.."))
import unittest, util.tests

def solve(puzzle_input):
    count = 0

    for passphrase in puzzle_input:
        words = passphrase.split(" ")
        if sorted(words) == sorted(set(words)):
            count += 1

    return count

def main():
    f = open("puzzle_input.txt")
    puzzle_input = f.read()[:-1].split("\n")
    f.close()

    count = solve(puzzle_input)

    print("The number of valid passphrases is " + str(count) + ".")

class AOC_Tests(unittest.TestCase):
    def test_ex1(self):
        self.assertEqual(solve(["aa bb cc dd ee", "aa bb cc dd aa", "aa bb cc dd aaa"]), 2)

if __name__ == "__main__":
    if unittest.main(verbosity=2, exit=False, testRunner=util.tests.Runner).result.wasSuccessful():
        main()
        exit(0)
    else:
        exit(1)
