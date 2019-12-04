#!/usr/bin/env python3

#Advent of Code
#2019 Day 4, Part 2
#Solution by James C. (https://github.com/JamesMCo)

import os, sys
sys.path.append(os.path.abspath("../.."))
import unittest, util.read
from util.tests import run

def solve(puzzle_input):
    def adjacency_rule(n):
        n = str(n)
        for i in range(len(n) - 1):
            if n[i] == n[i+1]:
                if i != 0 and n[i-1] == n[i]:
                    continue
                if i != len(n) - 2 and n[i+2] == n[i]:
                    continue
                return True

        return False

    def increase_rule(n):
        n = str(n)
        return n == "".join(sorted(n))

    count = 0
    for candidate in range(puzzle_input[0], puzzle_input[1] + 1):
        if len(str(candidate)) == 6 and adjacency_rule(candidate) and increase_rule(candidate):
           count += 1
    return count

def main():
    puzzle_input = [int(x) for x in util.read.as_string().split("-")]

    count = solve(puzzle_input)

    print("The number of passwords within the range given is " + str(count) + ".")

class AOC_Tests(unittest.TestCase):
    @unittest.skip("No test cases")
    def test_ex1(self):
        pass

run(main)
