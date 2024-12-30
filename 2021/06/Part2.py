#!/usr/bin/env python3

#Advent of Code
#2021 Day 6, Part 2
#Solution by James C. (https://github.com/JamesMCo)

import os, sys
sys.path.append(os.path.abspath("../.."))
import unittest, util.read
from util.tests import run

def solve(puzzle_input):
    class Lanternfish:
        def __init__(self, timer, count):
            self.timer = timer
            self.count = count

        def tick(self):
            if self.timer == 0:
                self.timer = 6
                return True
            else:
                self.timer -= 1
                return False
    
    fish = []
    def get_fish_by_timer(t):
        candidate = [f for f in fish if f.timer == t]
        if candidate:
            return candidate[0]
        else:
            new_fish = Lanternfish(t, 0)
            fish.append(new_fish)
            return new_fish

    for t in puzzle_input:
        get_fish_by_timer(t).count += 1

    for day in range(1, 257):
        # Tick timers of all fish
        new_fish_count = 0
        for f in fish:
            if f.tick():
                new_fish_count += f.count

        # When a timer ticks at 0, it resets to 6, but there might be another fish that ticked from 7 to 6
        # As a result, there might be multiple fish objects with a timer of 6 (which is bad, and defeats the
        # entire goal of having a single object for each timer!)
        # Therefore, we need to merge these objects in to one object, done here by getting the counts of both
        # existing objects, creating a new object with the sum of these, removing the existing objects from
        # the list, and adding the new one to the list.
        if len(duplicates := [(i, f) for i, f in enumerate(fish) if f.timer == 6]) > 1:
            replacement = Lanternfish(6, sum(f[1].count for f in duplicates))
            for f in duplicates[::-1]:
                fish.pop(f[0])
            fish.append(replacement)

        if new_fish_count:
            get_fish_by_timer(8).count += new_fish_count

    return sum(f.count for f in fish)

def main():
    puzzle_input = util.read.as_int_list(",")

    fish = solve(puzzle_input)

    print("The number of lanternfish after 256 days is " + str(fish) + ".")

class AOC_Tests(unittest.TestCase):
    def test_ex1(self):
        return self.assertEqual(solve([3,4,3,1,2]), 26984457539)

if __name__ == "__main__":
    run(main)
