#!/usr/bin/env python3

#Advent of Code
#Day 12, Part 1
#Solution by James C. (https://github.com/JamesMCo)

import os, sys
sys.path.append(os.path.abspath("../.."))
import unittest, util.tests

def solve(puzzle_input):
    programs = {}
    connections = ["0"]
    for p in puzzle_input:
        programs[p.split(" ")[0]] = " ".join(p.split(" ")[2:]).split(", ")

    added = True
    while added:
        added = False
        for c in connections:
            for p in programs[c]:
                if p not in connections:
                    connections.append(p)
                    added = True

    return len(connections)

def main():
    f = open("puzzle_input.txt")
    puzzle_input = f.read()[:-1].split("\n")
    f.close()

    programs = solve(puzzle_input)

    print("The number of programs in the group that contains 0 is " + str(programs) + ".")

class AOC_Tests(unittest.TestCase):
    def test_ex1(self):
        self.assertEqual(solve(["0 <-> 2",
                                "1 <-> 1",
                                "2 <-> 0, 3, 4",
                                "3 <-> 2, 4",
                                "4 <-> 2, 3, 6",
                                "5 <-> 6",
                                "6 <-> 4, 5"]), 6)

if __name__ == "__main__":
    if unittest.main(verbosity=2, exit=False, testRunner=util.tests.Runner).result.wasSuccessful():
        main()
        exit(0)
    else:
        exit(1)
