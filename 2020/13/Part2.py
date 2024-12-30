#!/usr/bin/env python3

#Advent of Code
#2020 Day 12, Part 2
#Solution by James C. (https://github.com/JamesMCo)

import os, sys
sys.path.append(os.path.abspath("../.."))
import unittest, util.read
from util.tests import run

def solve(puzzle_input):
    # Based heavily on an algorithm described in this reddit thread by /u/crocrococ
    # https://www.reddit.com/r/adventofcode/comments/kcb3bb
    #
    # My original solution was to brute force the answer, starting at the first multiple
    # of the largest bus number after 100,000,000,000,000 and incrementing in steps of
    # the largest bus number, but this proved slow to run (not reaching a solution after
    # approx. 70,000,000,000 iterations and 16+ hours of runtime)

    busses = [(offset, int(bus)) for offset, bus in enumerate(puzzle_input[1].split(",")) if bus != "x"]

    def time_to_bus(t, bus):
        t = t % bus
        if t == 0: return 0
        return bus - t
    
    def valid(t, bus):
        return time_to_bus(t+ bus[0], bus[1]) == 0

    timestamp = 0
    step = 1
    for b in busses:
        while True:
            if valid(timestamp, b):
                break
            timestamp += step
        step *= b[1]
    return timestamp

def main():
    puzzle_input = util.read.as_lines()

    timestamp = solve(puzzle_input)

    print("The earliest timestamp such that the busses leave one after another is " + str(timestamp) + ".")

class AOC_Tests(unittest.TestCase):
    def test_ex1(self):
        return self.assertEqual(solve([None, "7,13,x,x,59,x,31,19"]), 1068781)

    def test_ex2(self):
        return self.assertEqual(solve([None, "17,x,13,19"]), 3417)

    def test_ex3(self):
        return self.assertEqual(solve([None, "67,7,59,61"]), 754018)

    def test_ex4(self):
        return self.assertEqual(solve([None, "67,x,7,59,61"]), 779210)

    def test_ex5(self):
        return self.assertEqual(solve([None, "67,7,x,59,61"]), 1261476)

    def test_ex6(self):
        return self.assertEqual(solve([None, "1789,37,47,1889"]), 1202161486)

if __name__ == "__main__":
    run(main)
