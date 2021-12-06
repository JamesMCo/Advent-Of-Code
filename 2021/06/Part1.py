#!/usr/bin/env python3

#Advent of Code
#2021 Day 6, Part 1
#Solution by James C. (https://github.com/JamesMCo)

import os, sys
sys.path.append(os.path.abspath("../.."))
import unittest, util.read
from util.tests import run

def solve(puzzle_input):
    class Lanternfish:
        def __init__(self, timer):
            self.timer = timer

        def tick(self, new_fish_list):
            if self.timer == 0:
                self.timer = 6
                new_fish_list.append(Lanternfish(8))
            else:
                self.timer -= 1
    
    fish = [Lanternfish(f) for f in puzzle_input]

    for day in range(1, 81):
        new_fish = []

        for f in fish:
            f.tick(new_fish)

        fish += new_fish
    
    return len(fish)

def main():
    puzzle_input = util.read.as_int_list(",")

    fish = solve(puzzle_input)

    print("The number of lanternfish after 80 days is " + str(fish) + ".")

class AOC_Tests(unittest.TestCase):
    def test_ex1(self):
        return self.assertEqual(solve([3,4,3,1,2]), 5934)

run(main)
