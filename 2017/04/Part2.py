#!/usr/bin/env python3

#Advent of Code
#Day 4, Part 2
#Solution by James C. (https://github.com/JamesMCo)

import unittest
from itertools import permutations

def solve(puzzle_input):
    count = 0

    for passphrase in puzzle_input:
        words = passphrase.split(" ")
        if sorted(words) == sorted(set(words)):
            invalid = False
            for i in words:
                for perm in permutations(i):
                    if "".join(perm) != i and "".join(perm) in words:
                        invalid = True
                        break
                if invalid:
                    break
            if not invalid:
                count += 1

    return count

def main():    
    f = open("puzzle_input.txt")
    puzzle_input = f.read()[:-1].split("\n")
    f.close()

    count = solve(puzzle_input)

    print("The number of valid passphrases is " + str(count) + ".")

class AOC_Tests(unittest.TestCase):
    def test_ex1(self):
        self.assertEqual(solve(["abcde fghij", "abcde xyz ecdab", "a ab abc abd abf abj", "iiii oiii ooii oooi oooo", "oiii ioii iioi iiio"]), 3)

if __name__ == "__main__":
    if unittest.main(verbosity=2, exit=False).result.wasSuccessful():
        main()
        exit(0)
    else:
        exit(1)
