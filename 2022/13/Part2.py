#!/usr/bin/env python3

#Advent of Code
#2022 Day 13, Part 2
#Solution by James C. (https://github.com/JamesMCo)

import os, sys
sys.path.append(os.path.abspath("../.."))
import unittest, util.read
from util.tests import run

from ast import literal_eval
from functools import cmp_to_key
from itertools import zip_longest

def solve(puzzle_input):
    def compare(left, right):
        # If left should be before right/if in correct order, return -1
        # If neither should be before the other, return 0
        # If right should be before left/if in wrong order, return 1

        if type(left) == int and type(right) == int:
            if left < right:
                return -1
            elif left > right:
                return 1
            else:
                return 0
        
        if type(left) == int and type(right) == list:
            left = [left]
        elif type(left) == list and type(right) == int:
            right = [right]

        for left_val, right_val in zip_longest(left, right, fillvalue=None):
            if left_val == None:
                # Left ran out before right, correct order
                return -1
            elif right_val == None:
                # Right ran out before left, wrong order
                return 1

            if (comparison_result := compare(left_val, right_val)) != 0:
                return comparison_result

        # Neither left nor right should be before the other (otherwise, would have returned in the for loop)
        return 0

    sorted_packets = sorted([literal_eval(line) for line in puzzle_input if line != ""] + [[[2]], [[6]]], key=cmp_to_key(compare))
    return (sorted_packets.index([[2]]) + 1) * (sorted_packets.index([[6]]) + 1)

def main():
    puzzle_input = util.read.as_lines()

    decoder_key = solve(puzzle_input)

    print("The decoder key is " + str(decoder_key) + ".")

class AOC_Tests(unittest.TestCase):
    def test_ex1(self):
        return self.assertEqual(solve(["[1,1,3,1,1]",
                                       "[1,1,5,1,1]",
                                       "",
                                       "[[1],[2,3,4]]",
                                       "[[1],4]",
                                       "",
                                       "[9]",
                                       "[[8,7,6]]",
                                       "",
                                       "[[4,4],4,4]",
                                       "[[4,4],4,4,4]",
                                       "",
                                       "[7,7,7,7]",
                                       "[7,7,7]",
                                       "",
                                       "[]",
                                       "[3]",
                                       "",
                                       "[[[]]]",
                                       "[[]]",
                                       "",
                                       "[1,[2,[3,[4,[5,6,7]]]],8,9]",
                                       "[1,[2,[3,[4,[5,6,0]]]],8,9]"]), 140)

if __name__ == "__main__":
    run(main)
