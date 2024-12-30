#!/usr/bin/env python3

#Advent of Code
#2018 Day 7, Part 1
#Solution by James C. (https://github.com/JamesMCo)

import os, sys
sys.path.append(os.path.abspath("../.."))
import unittest, util.read
from util.tests import run

from collections import defaultdict

def solve(puzzle_input):
    steps = defaultdict(str)
    letters = set()
    for step in puzzle_input:
        step = step.split()
        letters.add(step[1])
        letters.add(step[7])
        steps[step[7]] += step[1]

    order = ""

    for i in range(len(letters)):
        chosen = sorted([x for x in letters if x not in steps and x not in order])[0]
        order += chosen

        to_remove = []
        for s in steps:
            steps[s] = steps[s].replace(chosen, "")
            if len(steps[s]) == 0:
                to_remove.append(s)
        for t in to_remove:
            del steps[t]

    return order

def main():
    puzzle_input = util.read.as_lines()

    order = solve(puzzle_input)

    print("The order to complete the steps is " + str(order) + ".")

class AOC_Tests(unittest.TestCase):
    def test_ex1(self):
        self.assertEqual(solve(["Step C must be finished before step A can begin.",
                                "Step C must be finished before step F can begin.",
                                "Step A must be finished before step B can begin.",
                                "Step A must be finished before step D can begin.",
                                "Step B must be finished before step E can begin.",
                                "Step D must be finished before step E can begin.",
                                "Step F must be finished before step E can begin."]), "CABDFE")

if __name__ == "__main__":
    run(main)
