#!/usr/bin/env python3

#Advent of Code
#2020 Day 18, Part 2
#Solution by James C. (https://github.com/JamesMCo)

import os, sys
sys.path.append(os.path.abspath("../.."))
import unittest, util.read
from util.tests import run

import string

def solve(puzzle_input):
    def parse(raw, start, end):
        i       = start
        working = ""
        tokens  = []
        while i < end:
            char    = raw[i]
            if char == " ":
                i += 1
            elif char in string.digits:
                j = i + 1
                while j < end and raw[j] in string.digits:
                    j += 1
                tokens.append(int(raw[i:j]))
                i = j
            elif char in "+*":
                tokens.append(char)
                i += 1
            elif char == "(":
                j = i + 1
                depth = 1
                while j < end and depth > 0:
                    if raw[j] == "(":
                        depth += 1
                    elif raw[j] == ")":
                        depth -= 1
                    j += 1
                tokens.append(parse(raw, i + 1, j - 1))
                i = j
        return tokens


    def evaluate(expr):
        if len(expr) == 0:
            return 0
        if len(expr) == 1:
            if type(expr[0]) == int:
                return expr[0]
            else:
                return evaluate(expr[0])

        while "+" in expr:
            if len(expr) == 3:
                return evaluate([expr[0]]) + evaluate([expr[2]])

            i = expr.index("+")
            expr = expr[:i-1] + [evaluate(expr[i-1:i+2])] + expr[i+2:]

        if expr[1] == "*":
            return evaluate([expr[0]]) * evaluate(expr[2:])

    return sum(evaluate(parse(e, 0, len(e))) for e in puzzle_input)

def main():
    puzzle_input = util.read.as_lines()

    value_sum = solve(puzzle_input)

    print("The sum of all of the expressions is " + str(value_sum) + ".")

class AOC_Tests(unittest.TestCase):
    def test_ex1(self):
        return self.assertEqual(solve(["1 + 2 * 3 + 4 * 5 + 6"]), 231)

    def test_ex2(self):
        return self.assertEqual(solve(["1 + (2 * 3) + (4 * (5 + 6))"]), 51)

    def test_ex3(self):
        return self.assertEqual(solve(["2 * 3 + (4 * 5)"]), 46)

    def test_ex4(self):
        return self.assertEqual(solve(["5 + (8 * 3 + 9 + 3 * 4 * 3)"]), 1445)

    def test_ex5(self):
        return self.assertEqual(solve(["5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4))"]), 669060)

    def test_ex6(self):
        return self.assertEqual(solve(["((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2"]), 23340)

run(main)
