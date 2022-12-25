#!/usr/bin/env python3

#Advent of Code
#2022 Day 25, Part 1
#Solution by James C. (https://github.com/JamesMCo)

import os, sys
sys.path.append(os.path.abspath("../.."))
import unittest, util.read
from util.tests import run

from itertools import zip_longest

def solve(puzzle_input):
    class SNAFU:
        @classmethod
        def from_list(cls, digits):
            n = SNAFU("0")
            n.val = digits
            return n

        def __init__(self, val):
            self.val = ["=-012".index(n) - 2 for n in val[::-1]]

        def __str__(self):
            return "".join("=-012"[n + 2] for n in self.val[::-1])

        def __add__(self, other):
            digits = []
            carry = 0
            for a, b in zip_longest(self.val, other.val, fillvalue=0):
                n = a + b + carry
                if n >= 3:
                    n -= 5
                    carry = 1
                elif n <= -3:
                    n += 5
                    carry = -1
                else:
                    carry = 0
                digits.append(n)
            digits.append(carry)

            while len(digits) > 1 and digits[-1] == 0:
                digits.pop()

            return SNAFU.from_list(digits)

    return str(sum((SNAFU(n) for n in puzzle_input[1:]), start=SNAFU(puzzle_input[0])))

def main():
    puzzle_input = util.read.as_lines()

    snafu_num = solve(puzzle_input)

    print("The SNAFU number to supply to Bob's console is " + str(snafu_num) + ".")

class AOC_Tests(unittest.TestCase):
    def test_ex1(self):
        return self.assertEqual(solve(["1=-0-2",
                                       "12111",
                                       "2=0=",
                                       "21",
                                       "2=01",
                                       "111",
                                       "20012",
                                       "112",
                                       "1=-1=",
                                       "1-12",
                                       "12",
                                       "1=",
                                       "122"]), "2=-1=0")

run(main)
