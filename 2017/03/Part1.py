#!/usr/bin/env python3

#Advent of Code
#Day 3, Part 1
#Solution by James C. (https://github.com/JamesMCo)

import unittest

def solve(puzzle_input):
    x = y = 0

    while ((x * 2) + 1) ** 2 <= puzzle_input:
        x += 1
        y += 1
    x -= 1
    y -= 1
    i = ((x * 2) + 1) ** 2

    max_coord = x

    stage = 3 #0 is moving up, 1 left, 2 down and 3 right
    while i < puzzle_input:
        if stage == 0:
            if y == -max_coord:
                stage = 1
            y -= 1
        elif stage == 1:
            if x == -max_coord:
                stage = 2
            x -= 1
        elif stage == 2:
            if y == max_coord:
                stage = 3
            y += 1
        elif stage == 3:
            if x == max_coord:
                stage = 0
            x += 1
        i += 1
    return abs(x) + abs(y)

def main():
    f = open("puzzle_input.txt")
    puzzle_input = int(f.read()[:-1])
    f.close()

    steps = solve(puzzle_input)

    print("The number of steps required is " + str(steps) + ".")

class AOC_Tests(unittest.TestCase):
    def test_ex1(self):
        self.assertEqual(solve(1), 0)

    def test_ex2(self):
        self.assertEqual(solve(12), 3)

    def test_ex3(self):
        self.assertEqual(solve(23), 2)

    def test_ex4(self):
        self.assertEqual(solve(1024), 31)

if __name__ == "__main__":
    if unittest.main(verbosity=2, exit=False).result.wasSuccessful():
        main()
        exit(0)
    else:
        exit(1)
