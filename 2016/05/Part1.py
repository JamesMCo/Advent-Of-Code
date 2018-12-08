#!/usr/bin/env python3

#Advent of Code
#2016 Day 5, Part 1
#Solution by James C. (https://github.com/JamesMCo)

import os, sys
sys.path.append(os.path.abspath("../.."))
import unittest, util.read
from util.tests import run

from hashlib import md5

def solve(puzzle_input):
    characters_found = 0
    password = ""
    current_index = 0

    while characters_found < 8:
        current_hash = md5(str(puzzle_input + str(current_index)).encode("utf-8")).hexdigest()
        if len(current_hash) > 5 and current_hash[:5] == "0"*5:
            password += current_hash[5]
            characters_found += 1
        current_index += 1

    return password

def main():
    puzzle_input = util.read.as_string()

    password = solve(puzzle_input)

    print("The password is " + password + ".")

class AOC_Tests(unittest.TestCase):
    def test_ex1(self):
        self.assertEqual(solve("abc"), "18f47a30")

run(main)
