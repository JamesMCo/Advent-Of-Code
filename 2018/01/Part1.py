#!/usr/bin/env python3

#Advent of Code
#Day 1, Part 1
#Solution by James C. (https://github.com/JamesMCo)

import os, sys, colorama, time
sys.path.append(os.path.abspath("../.."))
import unittest, util.tests

def solve(puzzle_input):
    freq = 0

    for f in puzzle_input:
        if f[0] == "+":
            freq += int(f[1:])
        else:
            freq -= int(f[1:])

    return freq

def main():
    f = open("puzzle_input.txt")
    puzzle_input = f.read().strip().split("\n")
    f.close()

    freq = solve(puzzle_input)

    print("The resulting frequency is " + str(freq) + ".")

class AOC_Tests(unittest.TestCase):
    def test_ex1(self):
        self.assertEqual(solve(["+1", "-2", "+3", "+1"]), 3)

    def test_ex2(self):
        self.assertEqual(solve(["+1", "+1", "-2"]), 0)

    def test_ex3(self):
        self.assertEqual(solve(["-1", "-2", "-3"]), -6)

if __name__ == "__main__":
    if unittest.main(verbosity=2, exit=False, testRunner=util.tests.Runner).result.wasSuccessful():
        start = time.time()
        main()
        end = time.time()
        print(f"{colorama.Fore.CYAN}Solution found in {colorama.Fore.GREEN}{round(end - start, 3)}s{colorama.Fore.CYAN}.{colorama.Fore.RESET}")
        exit(0)
    else:
        exit(1)
