#!/usr/bin/env python3

#Advent of Code
#Day 13, Part 1
#Solution by James C. (https://github.com/JamesMCo)

import os, sys
sys.path.append(os.path.abspath("../.."))
import unittest, util.tests

def solve(puzzle_input):
    layers = {}
    for l in puzzle_input:
        layers[int(l.split(": ")[0])] = int(l.split(": ")[1])
    severity = 0
    step = 0
    final = max(layers)

    while step <= final:
        if step in layers:
            if step % ((layers[step] - 1) * 2) == 0:
                severity += step * layers[step]
        step += 1

    return severity

def main():
    f = open("puzzle_input.txt")
    puzzle_input = f.read()[:-1].split("\n")
    f.close()

    severity = solve(puzzle_input)

    print("The severity of the whole trip is " + str(severity) + ".")

class AOC_Tests(unittest.TestCase):
    def test_ex1(self):
        self.assertEqual(solve(["0: 3",
                                "1: 2",
                                "4: 4",
                                "6: 4"]), 24)

if __name__ == "__main__":
    if unittest.main(verbosity=2, exit=False, testRunner=util.tests.Runner).result.wasSuccessful():
        main()
        exit(0)
    else:
        exit(1)
