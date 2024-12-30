#!/usr/bin/env python3

#Advent of Code
#2018 Day 8, Part 2
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

        def get_value(self):
            if self.count_children == 0:
                return sum(self.metadata)
            else:
                return sum(self.children[ref-1].get_value() for ref in self.metadata if ref > 0 and ref <= self.count_children)

    return LicenseNode(puzzle_input).get_value()

def main():
    puzzle_input = util.read.as_int_list(" ")

    root_value = solve(puzzle_input)

    print("The value of the root node is " + str(root_value) + ".")

class AOC_Tests(unittest.TestCase):
    def test_ex1(self):
        self.assertEqual(solve([2, 3, 0, 3, 10, 11, 12, 1, 1, 0, 1, 99, 2, 1, 1, 2]), 66)

if __name__ == "__main__":
    run(main)
