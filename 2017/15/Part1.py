#!/usr/bin/env python3

#Advent of Code
#Day 15, Part 1
#Solution by James C. (https://github.com/JamesMCo)

import unittest

def solve(puzzle_input):
    gena = puzzle_input[0]
    genb = puzzle_input[1]
    count = 0

    for i in range(40000000):
        gena = (gena * 16807) % 2147483647
        genb = (genb * 48271) % 2147483647

        if bin(gena)[2:].zfill(32)[16:] == bin(genb)[2:].zfill(32)[16:]:
            count += 1
    
    return count

def main():
    f = open("puzzle_input.txt")
    puzzle_input = [int(x.split(" ")[-1]) for x in f.read()[:-1].split("\n")]
    f.close()

    count = solve(puzzle_input)

    print("The judge's final count is " + str(count) + ".")

class AOC_Tests(unittest.TestCase):
    def test_ex1(self):
        self.assertEqual(solve([65, 8921]), 588)

if __name__ == "__main__":
    if unittest.main(verbosity=2, exit=False).result.wasSuccessful():
        main()
        exit(0)
    else:
        exit(1)