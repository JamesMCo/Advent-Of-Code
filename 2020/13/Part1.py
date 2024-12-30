#!/usr/bin/env python3

#Advent of Code
#2020 Day 12, Part 1
#Solution by James C. (https://github.com/JamesMCo)

import os, sys
sys.path.append(os.path.abspath("../.."))
import unittest, util.read
from util.tests import run

def solve(puzzle_input):
    earliest_time = int(puzzle_input[0])
    busses = [int(bus) for bus in puzzle_input[1].split(",") if bus != "x"]

    def time_to_bus(bus):
        t = earliest_time % bus
        if t == 0: return 0
        return bus - t

    busses.sort(key=time_to_bus)
    return busses[0] * time_to_bus(busses[0])

def main():
    puzzle_input = util.read.as_lines()

    id_waittime = solve(puzzle_input)

    print("The ID of the earliest bus multiplied by the minutes required to wait is " + str(id_waittime) + ".")

class AOC_Tests(unittest.TestCase):
    def test_ex1(self):
        return self.assertEqual(solve(["939", "7,13,x,x,59,x,31,19"]), 295)

if __name__ == "__main__":
    run(main)
