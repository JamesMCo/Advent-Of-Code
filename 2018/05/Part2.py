#!/usr/bin/env python3

#Advent of Code
#Day 5, Part 2
#Solution by James C. (https://github.com/JamesMCo)

import os, sys, colorama, time
sys.path.append(os.path.abspath("../.."))
import unittest, util.tests

import string

def solve(puzzle_input):
    def react(polymer):
        units = []
        for u in polymer:
            if len(units) > 0:
                if units[-1].swapcase() == u:
                    units.pop()
                else:
                    units.append(u)
            else:
                units.append(u)
        return "".join(units)

    lengths = []
    for u in string.ascii_lowercase:
        if u in puzzle_input.lower():
            lengths.append(len(react(puzzle_input.replace(u, "").replace(u.upper(), ""))))
    
    return min(lengths)

def main():
    f = open("puzzle_input.txt")
    puzzle_input = f.read()[:-1]
    f.close()

    units = solve(puzzle_input)

    print("The length of the shortest polymer you can produce is " + str(units) + ".")

class AOC_Tests(unittest.TestCase):
    def test_ex1(self):
        self.assertEqual(solve("dabAcCaCBAcCcaDA"), 4)

if __name__ == "__main__":
    if unittest.main(verbosity=2, exit=False, testRunner=util.tests.Runner).result.wasSuccessful():
        start = time.time()
        main()
        end = time.time()
        print(f"{colorama.Fore.CYAN}Solution found in {colorama.Fore.GREEN}{round(end - start, 3)}s{colorama.Fore.CYAN}.{colorama.Fore.RESET}")
        exit(0)
    else:
        exit(1)
