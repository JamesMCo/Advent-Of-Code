#!/usr/bin/env python3

#Advent of Code
#2015 Day 14, Part 1
#Solution by James C. (https://github.com/JamesMCo)

import os, sys
sys.path.append(os.path.abspath("../.."))
import unittest, util.read
from util.tests import run

def solve(puzzle_input, duration=2503):
    distances = []
    for reindeer in puzzle_input:
        reindeer = reindeer.split()

        t = 0
        d = 0
        speed = int(reindeer[3])
        flytime = int(reindeer[6])
        resttime = int(reindeer[13])
        state = "fly"

        while t + flytime < duration:
            if state == "fly":
                d += speed * flytime
                t += flytime
                state = "rest"
            elif state == "rest":
                t += resttime
                state = "fly"

        if state == "fly" and t < duration:
            d += speed * (duration - t)
        distances.append(d)

    return max(distances)

def main():
    puzzle_input = util.read.as_lines()

    highest = solve(puzzle_input)

    print("After 2503 seconds, the distance the winning reindeer has travelled is " + str(highest) + "km.")

class AOC_Tests(unittest.TestCase):
    def test_ex1(self):
        return self.assertEqual(solve(["Comet can fly 14 km/s for 10 seconds, but then must rest for 127 seconds.",
                                       "Dancer can fly 16 km/s for 11 seconds, but then must rest for 162 seconds."], 1), 16)

    def test_ex2(self):
        return self.assertEqual(solve(["Comet can fly 14 km/s for 10 seconds, but then must rest for 127 seconds.",
                                       "Dancer can fly 16 km/s for 11 seconds, but then must rest for 162 seconds."], 10), 160)

    def test_ex3(self):
        return self.assertEqual(solve(["Comet can fly 14 km/s for 10 seconds, but then must rest for 127 seconds.",
                                       "Dancer can fly 16 km/s for 11 seconds, but then must rest for 162 seconds."], 11), 176)

    def test_ex4(self):
        return self.assertEqual(solve(["Comet can fly 14 km/s for 10 seconds, but then must rest for 127 seconds.",
                                       "Dancer can fly 16 km/s for 11 seconds, but then must rest for 162 seconds."], 12), 176)

    def test_ex5(self):
        return self.assertEqual(solve(["Comet can fly 14 km/s for 10 seconds, but then must rest for 127 seconds.",
                                       "Dancer can fly 16 km/s for 11 seconds, but then must rest for 162 seconds."], 1000), 1120)

run(main)
