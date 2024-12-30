#!/usr/bin/env python3

#Advent of Code
#2018 Day 12, Part 2
#Solution by James C. (https://github.com/JamesMCo)

import os, sys
sys.path.append(os.path.abspath("../.."))
import unittest, util.read
from util.tests import run

from collections import defaultdict

def solve(puzzle_input):
    dot = lambda: "."

    start = 0
    pots = list(puzzle_input.pop(0).split()[2])
    puzzle_input.pop(0)
    
    rules = defaultdict(dot)
    for rule in puzzle_input:
        rules[rule.split()[0]] = rule.split()[2]
    
    seen = set()
    final = False
    penultimate_total = 0

    for gen in range(50_000_000_000):
        working = []
        start -= 2
        pots.insert(0, ".")
        pots.insert(0, ".")
        pots.append(".")
        pots.append(".")

        working.append(rules[".." + "".join(pots[:3])])
        working.append(rules["." + "".join(pots[:4])])
        for i in range(2, len(pots)-2):
            working.append(rules["".join(pots[i-2:i+3])])
        working.append(rules["".join(pots[-4:]) + "."])
        working.append(rules["".join(pots[-3:]) + ".."])

        pots = working

        if final:
            total = 0
            for i, pot in enumerate(pots):
                if pot == "#":
                    total += i + start

            diff = total - penultimate_total
            return total + (diff * (50_000_000_000 - (gen + 1)))

        temp = "".join(pots).strip(".")
        if temp in seen:
            penultimate_total = 0
            for i, pot in enumerate(pots):
                if pot == "#":
                    penultimate_total += i + start

            final = True
        else:
            seen.add(temp)

def main():
    puzzle_input = util.read.as_lines()

    pot_sum = solve(puzzle_input)

    print("The sum of the numbers of all pots which contain a plant is " + str(pot_sum) + ".")

class AOC_Tests(unittest.TestCase):
    @unittest.skip("No test cases")
    def test_ex1(self):
        pass

if __name__ == "__main__":
    run(main)
