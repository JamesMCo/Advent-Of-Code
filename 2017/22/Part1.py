#!/usr/bin/env python3

#Advent of Code
#Day 22, Part 1
#Solution by James C. (https://github.com/JamesMCo)

import os, sys
sys.path.append(os.path.abspath("../.."))
import unittest, util.tests

def solve(puzzle_input, steps=10000):
    count = 0
    grid = puzzle_input[:]
    direction = "u"
    x = int(len(grid) / 2)
    y = int(len(grid) / 2)

    left  = {"u": "l",
             "l": "d",
             "d": "r",
             "r": "u"}
    right = {"u": "r",
             "r": "d",
             "d": "l",
             "l": "u"}

    for s in range(steps):
        if grid[y][x] == ".":
            direction = left[direction]
            grid[y] = grid[y][:x] + "#" + grid[y][x+1:]
            count += 1
        else:
            direction = right[direction]
            grid[y] = grid[y][:x] + "." + grid[y][x+1:]

        if direction == "u":
            if y == 0:
                grid.insert(0, "."*len(grid[0]))
                y += 1
            y -= 1
        elif direction == "d":
            if y == len(grid) - 1:
                grid.append("."*len(grid[0]))
            y += 1
        elif direction == "l":
            if x == 0:
                for l in range(len(grid)):
                    grid[l] = "." + grid[l]
                x += 1
            x -= 1
        elif direction == "r":
            if x == len(grid[0]) - 1:
                for l in range(len(grid)):
                    grid[l] = grid[l] + "."
            x += 1

    return count

def main():
    f = open("puzzle_input.txt")
    puzzle_input = f.read()[:-1].split("\n")
    f.close()

    infections = solve(puzzle_input)

    print("The number of bursts of activity that caused an infection is " + str(infections) + ".")

class AOC_Tests(unittest.TestCase):
    def test_ex1(self):
        self.assertEqual(solve(["..#",
                                "#..",
                                "..."], 7), 5)

    def test_ex2(self):
        self.assertEqual(solve(["..#",
                                "#..",
                                "..."], 70), 41)

    def test_ex3(self):
        self.assertEqual(solve(["..#",
                                "#..",
                                "..."], 10000), 5587)

if __name__ == "__main__":
    if unittest.main(verbosity=2, exit=False, testRunner=util.tests.Runner).result.wasSuccessful():
        main()
        exit(0)
    else:
        exit(1)
