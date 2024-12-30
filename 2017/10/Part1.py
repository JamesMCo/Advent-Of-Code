#!/usr/bin/env python3

#Advent of Code
#2017 Day 10, Part 1
#Solution by James C. (https://github.com/JamesMCo)

import os, sys
sys.path.append(os.path.abspath("../.."))
import unittest, util.read
from util.tests import run

def solve(puzzle_input, size=256):
    def rotate(l, n):
        t = [x for x in l]
        if len(t) <= 1:
            return t
        if len(t) == 2:
            return t[1] + t[0]
        for i in range(n):
            t = t[1:] + [t[0]]
        return t

    l = [x for x in range(size)]
    skip_size = 0

    for i in puzzle_input:
        if i <= size:
            l = l[i-1::-1] + l[i:]
        else:
            l = l[::-1]
        l = rotate(l, i + skip_size)
        skip_size += 1

    for i in puzzle_input:
        l = rotate(l, size - i + 1)
    return l[0] * l[1]

def main():
    puzzle_input = [int(x) for x in util.read.as_string().split(",")]

    product = solve(puzzle_input)

    print("The result of multiplying the first two numbers in the list is " + str(product) + ".")

class AOC_Tests(unittest.TestCase):
    def test_ex1(self):
        self.assertEqual(solve([3, 4, 1, 5], 5), 12)

if __name__ == "__main__":
    run(main)
