#!/usr/bin/env python3

#Advent of Code
#2016 Day 14, Part 2
#Solution by James C. (https://github.com/JamesMCo)

import os, sys
sys.path.append(os.path.abspath("../.."))
import unittest, util.read
from util.tests import run

from hashlib import md5

hashes = {}

def solve(puzzle_input):
    keys = 0
    i = 0

    def stretch(s):
        global hashes

        if s not in hashes:
            temp = md5(str(s).encode("utf-8")).hexdigest()

            for i in range(2016):
                temp = md5(str(temp).encode("utf-8")).hexdigest()

            hashes[s] = temp
        return hashes[s]

    while keys < 64:
        current_hash = stretch(puzzle_input + str(i))
        for c in range(len(current_hash)):
            try:
                if current_hash[c] == current_hash[c+1] == current_hash[c+2]:
                    for j in range(1, 1001):
                        if current_hash[c]*5 in stretch(puzzle_input + str(i+j)):
                            keys += 1
                            break
                    break
            except:
                pass
        i += 1

    return i - 1

def main():
    puzzle_input = util.read.as_string()

    index = solve(puzzle_input)

    print("The index that generates the 64th key is " + str(index) + ".")

class AOC_Tests(unittest.TestCase):
    def test_ex1(self):
        self.assertEqual(solve("abc"), 22551)

run(main)
