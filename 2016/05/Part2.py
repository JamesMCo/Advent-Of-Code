#!/usr/bin/env python3

#Advent of Code
#2016 Day 5, Part 2
#Solution by James C. (https://github.com/JamesMCo)

import os, sys
sys.path.append(os.path.abspath("../.."))
import unittest, util.read
from util.tests import run

from hashlib import md5
from random import choice
from string import ascii_letters, punctuation

def solve(puzzle_input):
    print()

    def printpass(replace=True):
        if replace: print("\x1b[1A\x1b[2K", end="")
        print("The password is ", end="")
        for i in password:
            if i != "_":
                print(i, end="")
            else:
                print(choice(ascii_letters + punctuation), end="")
        print(".")

    password = ["_" for i in range(8)]
    current_index = 0
    printpass(False)

    while "_" in password:
        current_hash = md5(str(puzzle_input + str(current_index)).encode("utf-8")).hexdigest()
        if len(current_hash) > 5 and current_hash[:5] == "0"*5 and 0 <= int(current_hash[5], 16) <= 7 and password[int(current_hash[5], 16)] == "_":
            password[int(current_hash[5], 16)] = current_hash[6]
            printpass()
            current_index += 1
            continue
        if current_index % 15000 == 0:
            printpass()
        current_index += 1

    return "".join(password)

def main():
    puzzle_input = util.read.as_string()

    solve(puzzle_input)

class AOC_Tests(unittest.TestCase):
    def test_ex1(self):
        self.assertEqual(solve("abc"), "05ace8e3")

if __name__ == "__main__":
    run(main)
