#!/usr/bin/env python3

#Advent of Code
#2015 Day 14, Part 2
#Solution by James C. (https://github.com/JamesMCo)

import os, sys
sys.path.append(os.path.abspath("../.."))
import unittest, util.read
from util.tests import run

def solve(puzzle_input, duration=2503):
    stats = []
    for reindeer in puzzle_input:
            reindeer = reindeer.split()

            stats.append({"t": 0,
                          "d": 0,
                          "speed": int(reindeer[3]),
                          "flytime": int(reindeer[6]),
                          "resttime": int(reindeer[13]),
                          "state": "fly",
                          "points": 0})

    for second in range(duration):
        for i in range(len(stats)):
            if stats[i]["state"] == "fly":
                stats[i]["d"] += stats[i]["speed"]
                stats[i]["t"] += 1
                if stats[i]["t"] == stats[i]["flytime"]:
                    stats[i]["t"] = 0
                    stats[i]["state"] = "rest"

            elif stats[i]["state"] == "rest":
                stats[i]["t"] += 1
                if stats[i]["t"] == stats[i]["resttime"]:
                    stats[i]["t"] = 0
                    stats[i]["state"] = "fly"

        first = max(reindeer["d"] for reindeer in stats)
        for i in range(len(stats)):
            if stats[i]["d"] == first:
                stats[i]["points"] += 1

    return max(reindeer["points"] for reindeer in stats)

def main():
    puzzle_input = util.read.as_lines()

    highest = solve(puzzle_input)

    print("After 2503 seconds, the number of points the winning reindeer has is " + str(highest) + ".")

class AOC_Tests(unittest.TestCase):
    def test_ex1(self):
        return self.assertEqual(solve(["Comet can fly 14 km/s for 10 seconds, but then must rest for 127 seconds.",
                                       "Dancer can fly 16 km/s for 11 seconds, but then must rest for 162 seconds."], 1), 1)

    def test_ex2(self):
        return self.assertEqual(solve(["Comet can fly 14 km/s for 10 seconds, but then must rest for 127 seconds.",
                                       "Dancer can fly 16 km/s for 11 seconds, but then must rest for 162 seconds."], 140), 139)

    def test_ex3(self):
        return self.assertEqual(solve(["Comet can fly 14 km/s for 10 seconds, but then must rest for 127 seconds.",
                                       "Dancer can fly 16 km/s for 11 seconds, but then must rest for 162 seconds."], 1000), 689)

run(main)
