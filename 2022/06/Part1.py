#!/usr/bin/env python3

#Advent of Code
#2022 Day 6, Part 1
#Solution by James C. (https://github.com/JamesMCo)

import os, sys
sys.path.append(os.path.abspath("../.."))
import unittest, util.read
from util.tests import run

def solve(puzzle_input):
    n = 4

    for i in range(n, len(puzzle_input)):
        if len(set(puzzle_input[i-n:i])) == n:
            return i

def main():
    puzzle_input = util.read.as_string()

    characters = solve(puzzle_input)

    print("The number of characters that need to be processed before the first start-of-packet marker is detected is " + str(characters) + ".")

class AOC_Tests(unittest.TestCase):
    def test_ex1(self):
        return self.assertEqual(solve("mjqjpqmgbljsphdztnvjfqwrcgsmlb"), 7)

    def test_ex2(self):
        return self.assertEqual(solve("bvwbjplbgvbhsrlpgdmjqwftvncz"), 5)

    def test_ex3(self):
        return self.assertEqual(solve("nppdvjthqldpwncqszvftbrmjlhg"), 6)

    def test_ex4(self):
        return self.assertEqual(solve("nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg"), 10)

    def test_ex5(self):
        return self.assertEqual(solve("zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw"), 11)

if __name__ == "__main__":
    run(main)
