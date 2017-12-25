#!/usr/bin/env python3

#Advent of Code
#Day 24, Part 1
#Solution by James C. (https://github.com/JamesMCo)

import os, sys
sys.path.append(os.path.abspath("../.."))
import unittest, util.tests

def solve(puzzle_input):
    def find_largest(parts, start, cur_strength):
        strongest = cur_strength

        if len(parts) == 0:
            return 0

        for i in range(len(parts)):
            if start in parts[i]:
                temp = find_largest(parts[:i] + parts[i+1:], parts[i][not parts[i].index(start)], cur_strength + parts[i][0] + parts[i][1])
                if temp > strongest:
                    strongest = temp

        return strongest

    parts = [sorted([int(x.split("/")[0]), int(x.split("/")[1])]) for x in puzzle_input]

    return find_largest(parts, 0, 0)

def main():
    f = open("puzzle_input.txt")
    puzzle_input = f.read()[:-1].split("\n")
    f.close()

    strongest = solve(puzzle_input)

    print("The strongest bridge that can be made has a strength of " + str(strongest) + ".")

class AOC_Tests(unittest.TestCase):
    def test_ex1(self):
        self.assertEqual(solve(["0/2",
                                "2/2",
                                "2/3",
                                "3/4",
                                "3/5",
                                "0/1",
                                "10/1",
                                "9/10"]), 31)

if __name__ == "__main__":
    if unittest.main(verbosity=2, exit=False, testRunner=util.tests.Runner).result.wasSuccessful():
        main()
        exit(0)
    else:
        exit(1)
