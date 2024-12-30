#!/usr/bin/env python3

#Advent of Code
#2015 Day 18, Part 1
#Solution by James C. (https://github.com/JamesMCo)

import os, sys
sys.path.append(os.path.abspath("../.."))
import unittest, util.read
from util.tests import run

def solve(puzzle_input):
    base = puzzle_input[-1]
    replacements = {}
    for replacement in puzzle_input[:-2]:
        replacement = replacement.split()
        if replacement[0] not in replacements:
            replacements[replacement[0]] = [replacement[2]]
        else:
            replacements[replacement[0]].append(replacement[2])

    longest = max(len(x) for x in replacements)
    found = []
    for i in range(len(base)):
        for j in range(1, longest+1):
            if i + j <= len(base):
                if base[i:i+j] in replacements:
                    for case in replacements[base[i:i+j]]:
                        if base[:i] + case + base[i+j:] not in found:
                            found.append(base[:i] + case + base[i+j:])

    return len(found)

def main():
    puzzle_input = util.read.as_string_list("\n")

    molecules = solve(puzzle_input)

    print("The number of distinct molecules the medicine molecule allows for is " + str(molecules) + ".")

class AOC_Tests(unittest.TestCase):
    def test_ex1(self):
        return self.assertEqual(solve(["H => HO",
                                       "H => OH",
                                       "O => HH",
                                       "",
                                       "HOH"]), 4)

    def test_ex2(self):
        return self.assertEqual(solve(["H => HO",
                                       "H => OH",
                                       "O => HH",
                                       "",
                                       "HOHOHO"]), 7)

if __name__ == "__main__":
    run(main)
