#!/usr/bin/env python3

#Advent of Code
#2021 Day 3, Part 2
#Solution by James C. (https://github.com/JamesMCo)

import os, sys
sys.path.append(os.path.abspath("../.."))
import unittest, util.read
from util.tests import run

from collections import Counter

def solve(puzzle_input):
    def find_rating(rating):
        # rating: 1 => oxygen (most common, 1 in a tie), 0 => co2 (least common, 0 in a tie)

        candidates = puzzle_input[:]
        i = 0
        while len(candidates) > 1:
            count = Counter()
            for number in candidates:
                count.update(number[i])
                
            results = count.most_common(2)
            if results[0][1] == results[-1][1] and results[0][0] != results[-1][0]:
                criteria = str(rating)
            else:
                criteria = count.most_common()[1-rating][0]

            candidates = [n for n in candidates if n[i] == criteria]
            i += 1


        return int(candidates[0], 2)
    
    oxygen = find_rating(1)
    co2 = find_rating(0)
    return oxygen * co2

def main():
    puzzle_input = util.read.as_lines()

    lifesupport = solve(puzzle_input)

    print("The life support rating is " + str(lifesupport) + ".")

class AOC_Tests(unittest.TestCase):
    def test_ex1(self):
        return self.assertEqual(solve(["00100",
                                       "11110",
                                       "10110",
                                       "10111",
                                       "10101",
                                       "01111",
                                       "00111",
                                       "11100",
                                       "10000",
                                       "11001",
                                       "00010",
                                       "01010"]), 230)

if __name__ == "__main__":
    run(main)
