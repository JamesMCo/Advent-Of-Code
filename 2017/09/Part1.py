#!/usr/bin/env python3

#Advent of Code
#Day 9, Part 1
#Solution by James C. (https://github.com/JamesMCo)

import os, sys
sys.path.append(os.path.abspath("../.."))
import unittest
from util.tests import run

def solve(puzzle_input):
    depth = 0
    total = 0

    i = 0
    while i < len(puzzle_input):
        if puzzle_input[i] == "!":
            puzzle_input = puzzle_input[:i] + puzzle_input[i+2:]
        else:
            i += 1        

    i = 0
    in_garbage = False
    while i < len(puzzle_input):
        if in_garbage:
            if puzzle_input[i] == ">":
                in_garbage = False
            puzzle_input = puzzle_input[:i] + puzzle_input[i+1:]
        elif puzzle_input[i] == "<":
            in_garbage = True
            puzzle_input = puzzle_input[:i] + puzzle_input[i+1:]
        else:
            i += 1

    for i in puzzle_input:
        if i == "{":
            depth += 1
            total += depth
        elif i == "}":
            if depth > 0:
                depth -= 1

    return total

def main():
    f = open("puzzle_input.txt")
    puzzle_input = f.read()[:-1]
    f.close()

    score = solve(puzzle_input)

    print("The total score for all groups in the input is " + str(score) + ".")

class AOC_Tests(unittest.TestCase):
    def test_ex1(self):
        self.assertEqual(solve("{}"), 1)

    def test_ex2(self):
        self.assertEqual(solve("{{{}}}"), 6)

    def test_ex3(self):
        self.assertEqual(solve("{{},{}}"), 5)

    def test_ex4(self):
        self.assertEqual(solve("{{{},{},{{}}}}"), 16)

    def test_ex5(self):
        self.assertEqual(solve("{<a>,<a>,<a>,<a>}"), 1)

    def test_ex6(self):
        self.assertEqual(solve("{{<ab>},{<ab>},{<ab>},{<ab>}}"), 9)

    def test_ex7(self):
        self.assertEqual(solve("{{<!!>},{<!!>},{<!!>},{<!!>}}"), 9)

    def test_ex8(self):
        self.assertEqual(solve("{{<a!>},{<a!>},{<a!>},{<ab>}}"), 3)

run(main)
