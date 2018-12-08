#!/usr/bin/env python3

#Advent of Code
#Day 4, Part 2
#Solution by James C. (https://github.com/JamesMCo)

import os, sys
sys.path.append(os.path.abspath("../.."))
import unittest, util.read
from util.tests import run

from collections import defaultdict

def solve(puzzle_input):
    puzzle_input.sort()
    sleeps = []
    current_sleep = None

    for event in puzzle_input:
        event = event.split()
        if event[2] == "Guard":
            current_guard = int(event[3][1:])
        elif event[2] == "falls":
            current_sleep = event[1][:-1]
        else:
            if event[1][:-1][:2] == "23":
                duration = 60 - int(event[1][:-1][3:5]) + int(current_sleep[3:])
            else:
                duration = int(event[1][:-1][3:5]) - int(current_sleep[3:])

            sleeps.append((current_guard, current_sleep, event[1][:-1], duration))

            current_sleep = None

    minutes = defaultdict(int)
    for sleep in sleeps:
        t = f"{sleep[0]}:" + sleep[1]
        while t != f"{sleep[0]}:" + sleep[2]:
            minutes[t] += 1

            t = t.split(":")
            if t[2] == "59":
                t = f"{t[0]}:{str(int(t[1])+1).zfill(2)}:00"
            else:
                t = f"{t[0]}:{t[1]}:{str(int(t[2])+1).zfill(2)}"
    chosen_minutes = max(minutes, key=lambda x: minutes[x])

    return int(chosen_minutes.split(":")[0]) * int(chosen_minutes.split(":")[2])

def main():
    puzzle_input = util.read.as_lines()

    product = solve(puzzle_input)

    print("The id of the guard chosen multiplied by the minute chosen is " + str(product) + ".")

class AOC_Tests(unittest.TestCase):
    def test_ex1(self):
        self.assertEqual(solve(["[1518-11-01 00:00] Guard #10 begins shift",
                                "[1518-11-01 00:05] falls asleep",
                                "[1518-11-01 00:25] wakes up",
                                "[1518-11-01 00:30] falls asleep",
                                "[1518-11-01 00:55] wakes up",
                                "[1518-11-01 23:58] Guard #99 begins shift",
                                "[1518-11-02 00:40] falls asleep",
                                "[1518-11-02 00:50] wakes up",
                                "[1518-11-03 00:05] Guard #10 begins shift",
                                "[1518-11-03 00:24] falls asleep",
                                "[1518-11-03 00:29] wakes up",
                                "[1518-11-04 00:02] Guard #99 begins shift",
                                "[1518-11-04 00:36] falls asleep",
                                "[1518-11-04 00:46] wakes up",
                                "[1518-11-05 00:03] Guard #99 begins shift",
                                "[1518-11-05 00:45] falls asleep",
                                "[1518-11-05 00:55] wakes up"]), 4455)

run(main)
