#!/usr/bin/env python3

#Advent of Code
#2018 Day 8, Part 1
#Solution by James C. (https://github.com/JamesMCo)

import os, sys
sys.path.append(os.path.abspath("../.."))
import unittest, util.read
from util.tests import run

def solve(puzzle_input):
    class LicenseNode:
        def __init__(self, data):
            self.count_children = data.pop(0)
            self.count_metadata = data.pop(0)
            self.children = []
            self.metadata = []

            for i in range(self.count_children): #Children nodes
                self.children.append(LicenseNode(data))
            for i in range(self.count_metadata): #Metadata entries
                self.metadata.append(data.pop(0))

        def get_metadata_sum(self):
            return sum(self.metadata) + sum(child.get_metadata_sum() for child in self.children)

    return LicenseNode(puzzle_input).get_metadata_sum()

def main():
    puzzle_input = util.read.as_int_list(" ")

    metadata_sum = solve(puzzle_input)

    print("The sum of all the metadata entries is " + str(metadata_sum) + ".")

class AOC_Tests(unittest.TestCase):
    def test_ex1(self):
        self.assertEqual(solve([2, 3, 0, 3, 10, 11, 12, 1, 1, 0, 1, 99, 2, 1, 1, 2]), 138)

if __name__ == "__main__":
    run(main)
