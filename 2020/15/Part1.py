#!/usr/bin/env python3

#Advent of Code
#2020 Day 15, Part 1
#Solution by James C. (https://github.com/JamesMCo)

import os, sys
sys.path.append(os.path.abspath("../.."))
import unittest, util.read
from util.tests import run

def solve(puzzle_input):
    said = {}
    last_said = puzzle_input[-1]

    def say(i, n):
        if n in said:
            said[n] = (i, said[n][0])
        else:
            said[n] = (i, None)

    for i, n in enumerate(puzzle_input):
        say(i, n)

    for i in range(len(puzzle_input), 2020):
        if said[last_said][1] == None:
            say(i, 0)
            last_said = 0
        else:
            diff = said[last_said][0] - said[last_said][1]
            say(i, diff)
            last_said = diff

    return last_said

def main():
    puzzle_input = util.read.as_int_list(",")

    spoken = solve(puzzle_input)

    print("The 2020th number spoken is " + str(spoken) + ".")

class AOC_Tests(unittest.TestCase):
    def test_ex1(self):
        return self.assertEqual(solve([0, 3, 6]), 436)
        
    def test_ex2(self):
        return self.assertEqual(solve([1, 3, 2]), 1)
        
    def test_ex3(self):
        return self.assertEqual(solve([2, 1, 3]), 10)
        
    def test_ex4(self):
        return self.assertEqual(solve([1, 2, 3]), 27)
        
    def test_ex5(self):
        return self.assertEqual(solve([2, 3, 1]), 78)
        
    def test_ex6(self):
        return self.assertEqual(solve([3, 2, 1]), 438)
        
    def test_ex7(self):
        return self.assertEqual(solve([3, 1, 2]), 1836)

run(main)
