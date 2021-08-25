#!/usr/bin/env python3

#Advent of Code
#2015 Day 12, Part 2
#Solution by James C. (https://github.com/JamesMCo)

import os, sys
sys.path.append(os.path.abspath("../.."))
import unittest, util.read
from util.tests import run
import json

def solve(puzzle_input):
    output = 0
    
    if type(puzzle_input) == type({}):
        red = False
        for element in puzzle_input:
            if puzzle_input[element] == "red":
                red = True
                break
            elif type(puzzle_input[element]) == type(0):
                output += puzzle_input[element]
            elif type(puzzle_input[element]) in [type({}), type([])]:
                output += solve(puzzle_input[element])

        if red:
            output = 0
    elif type(puzzle_input) == type([]):
        for element in puzzle_input:
            if type(element) == type(0):
                output += element
            elif type(element) in [type({}), type([])]:
                output += solve(element)

    return output

def main():
    puzzle_input = json.loads(util.read.as_string())

    total = solve(puzzle_input)

    print("The final total is " + str(total) + ".")

class AOC_Tests(unittest.TestCase):
    def test_ex1(self):
        return self.assertEqual(solve([1,2,3]), 6)

    def test_ex2(self):
        return self.assertEqual(solve([1,{"c":"red","b":2},3]), 4)

    def test_ex3(self):
        return self.assertEqual(solve({"d":"red","e":[1,2,3,4],"f":5}), 0)

    def test_ex4(self):
        return self.assertEqual(solve([1,"red",5]), 6)

run(main)
