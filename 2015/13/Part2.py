#!/usr/bin/env python3

#Advent of Code
#2015 Day 13, Part 2
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
    for person in people:
        units[f"{person},You"] = 0
        units[f"You,{person}"] = 0
    people.append("You")

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
    @unittest.skip("No test cases")
    def test_ex1(self):
        pass

if __name__ == "__main__":
    run(main)
