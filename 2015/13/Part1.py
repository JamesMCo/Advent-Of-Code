#!/usr/bin/env python3

#Advent of Code
#2015 Day 13, Part 1
#Solution by James C. (https://github.com/JamesMCo)

import os, sys
sys.path.append(os.path.abspath("../.."))
import unittest, util.read
from util.tests import run
from itertools import permutations

def solve(puzzle_input):
    people = []
    units = {}
    for line in puzzle_input:
        line = line.split()
        for person in [line[0], line[-1][:-1]]:
            if person not in people:
                people.append(person)
        if line[2] == "gain":
            units[f"{line[0]},{line[-1][:-1]}"] = int(line[3])
        else:
            units[f"{line[0]},{line[-1][:-1]}"] = -int(line[3])

    def sat(a, b):
        return units[f"{a},{b}"] + units[f"{b},{a}"]

    highest = 0
    for arr in permutations(people):
        running = 0
        temp = list(arr[1:])
        temp.append(arr[0])
        for a, b in zip(arr, temp):
            running += sat(a, b)
        if running > highest:
            highest = running

    return highest

def main():
    puzzle_input = util.read.as_lines()

    highest = solve(puzzle_input)

    print("The total change in happiness for the optimal seating arrangement is " + str(highest) + ".")

class AOC_Tests(unittest.TestCase):
    def test_ex1(self):
        return self.assertEqual(solve(["Alice would gain 54 happiness units by sitting next to Bob.",
                                       "Alice would lose 79 happiness units by sitting next to Carol.",
                                       "Alice would lose 2 happiness units by sitting next to David.",
                                       "Bob would gain 83 happiness units by sitting next to Alice.",
                                       "Bob would lose 7 happiness units by sitting next to Carol.",
                                       "Bob would lose 63 happiness units by sitting next to David.",
                                       "Carol would lose 62 happiness units by sitting next to Alice.",
                                       "Carol would gain 60 happiness units by sitting next to Bob.",
                                       "Carol would gain 55 happiness units by sitting next to David.",
                                       "David would gain 46 happiness units by sitting next to Alice.",
                                       "David would lose 7 happiness units by sitting next to Bob.",
                                       "David would gain 41 happiness units by sitting next to Carol."]), 330)

if __name__ == "__main__":
    run(main)
