#!/usr/bin/env python3

#Advent of Code
#Day 2, Part 1
#Solution by James C. (https://github.com/JamesMCo)

import os, sys, colorama, time
sys.path.append(os.path.abspath("../.."))
import unittest, util.tests

import string

def solve(puzzle_input):
    twos = 0
    threes = 0

    for i in puzzle_input:
        if sum([1 for x in string.ascii_lowercase if i.count(x) == 2]) >= 1:
            twos += 1

        if sum([1 for x in string.ascii_lowercase if i.count(x) == 3]) >= 1:
            threes += 1
    
    return twos * threes

def main():
    f = open("puzzle_input.txt")
    puzzle_input = f.read()[:-1].split("\n")
    f.close()

    checksum = solve(puzzle_input)

    print("The checksum is " + str(checksum) + ".")

class AOC_Tests(unittest.TestCase):
    def test_ex1(self):
        self.assertEqual(solve(["abcdef"
                                "bababc",
                                "abbcde",
                                "abcccd",
                                "aabcdd",
                                "abcdee",
                                "ababab"]), 12)

if __name__ == "__main__":
    if unittest.main(verbosity=2, exit=False, testRunner=util.tests.Runner).result.wasSuccessful():
        start = time.time()
        main()
        end = time.time()
        print(f"{colorama.Fore.CYAN}Solution found in {colorama.Fore.GREEN}{round(end - start, 3)}s{colorama.Fore.CYAN}.{colorama.Fore.RESET}")
        exit(0)
    else:
        exit(1)
