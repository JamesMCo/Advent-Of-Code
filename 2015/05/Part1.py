#!/usr/bin/env python3

#Advent of Code
#2015 Day 5, Part 1
#Solution by James C. (https://github.com/JamesMCo)

import os, sys
sys.path.append(os.path.abspath("../.."))
import unittest, util.read
from util.tests import run

def solve(puzzle_input):
    nice = 0

    for i in puzzle_input:
        vowels = 0
        vowels += list(i).count("a")
        vowels += list(i).count("e")
        vowels += list(i).count("i")
        vowels += list(i).count("o")
        vowels += list(i).count("u")

        doubles = False
        for x in range(97, 123):
            if chr(x)*2 in i:
                doubles = True

        badstring = False
        for x in ["ab", "cd", "pq", "xy"]:
            if x in i:
                badstring = True

        if vowels >= 3 and doubles == True and badstring == False:
            nice += 1

    return nice

def main():
    puzzle_input = util.read.as_lines()

    nice = solve(puzzle_input)

    print("The number of nice strings is " + str(nice) + ".")

class AOC_Tests(unittest.TestCase):
    def test_ex1(self):
        return self.assertEqual(solve(["ugknbfddgicrmopn"]), 1)

    def test_ex2(self):
        return self.assertEqual(solve(["aaa"]), 1)

    def test_ex3(self):
        return self.assertEqual(solve(["jchzalrnumimnmhp"]), 0)

    def test_ex4(self):
        return self.assertEqual(solve(["haegwjzuvuyypxyu"]), 0)

    def test_ex5(self):
        return self.assertEqual(solve(["dvszwmarrgswjxmb"]), 0)

if __name__ == "__main__":
    run(main)
