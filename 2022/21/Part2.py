#!/usr/bin/env python3

#Advent of Code
#2022 Day 21, Part 2
#Solution by James C. (https://github.com/JamesMCo)

import os, sys
sys.path.append(os.path.abspath("../.."))
import unittest, util.read
from util.tests import run

import re

def solve(puzzle_input):
    class Monkey:
        monkeys = {}

        number_pattern = re.compile("(\w+): (\d+)")
        math_pattern   = re.compile("(\w+): (\w+) ([\+\-\*\/]) (\w+)")

        def __init__(self, description):
            self.name = None
            self.val  = None

            self.dependencies = []
            self.operation    = None

            if description.startswith("humn"):
                self.name = "humn"
            elif (match := re.match(Monkey.number_pattern, description)):
                groups = match.groups()
                self.name = groups[0]
                self.val  = int(groups[1])
            elif (match := re.match(Monkey.math_pattern, description)):
                groups = match.groups()
                self.name = groups[0]
                self.dependencies = [groups[1], groups[3]]
                if self.name == "root":
                    self.operation = "="
                else:
                    self.operation = groups[2]

            Monkey.monkeys[self.name] = self

        def get_val(self):
            if self.val:
                return self.val

            match self.operation:
                case "+":
                    return Monkey.monkeys[self.dependencies[0]].get_val() + Monkey.monkeys[self.dependencies[1]].get_val()
                case "-":
                    return Monkey.monkeys[self.dependencies[0]].get_val() - Monkey.monkeys[self.dependencies[1]].get_val()
                case "*":
                    return Monkey.monkeys[self.dependencies[0]].get_val() * Monkey.monkeys[self.dependencies[1]].get_val()
                case "/":
                    result = Monkey.monkeys[self.dependencies[0]].get_val() / Monkey.monkeys[self.dependencies[1]].get_val()
                    if result == int(result):
                        return int(result)
                    else:
                        return result
                case None:
                    return None

        def depends_on_humn(self):
            if self.val:
                return False
            elif "humn" in self.dependencies:
                return True
            else:
                return Monkey.monkeys[self.dependencies[0]].depends_on_humn() or Monkey.monkeys[self.dependencies[1]].depends_on_humn()

        def __str__(self):
            if self.name == "humn":
                return "humn"
            elif not self.depends_on_humn():
                return str(self.get_val())

            left_val  = str(Monkey.monkeys[self.dependencies[0]])
            right_val = str(Monkey.monkeys[self.dependencies[1]])

            match self.operation:
                case "+":
                    return f"({left_val} + {right_val})"
                case "-":
                    return f"({left_val} - {right_val})"
                case "*":
                    return f"({left_val} * {right_val})"
                case "/":
                    return f"({left_val} / {right_val})"
                case "=":
                    return f"{left_val} = {right_val}"

        def to_equation(self):
            if self.name == "humn":
                return "humn"
            elif not self.depends_on_humn():
                return self.get_val()

            left_val  = Monkey.monkeys[self.dependencies[0]].to_equation()
            right_val = Monkey.monkeys[self.dependencies[1]].to_equation()

            match self.operation:
                case "+":
                    return (left_val, "+", right_val)
                case "-":
                    return (left_val, "-", right_val)
                case "*":
                    return (left_val, "*", right_val)
                case "/":
                    return (left_val, "/", right_val)
                case "=":
                    return (left_val, "=", right_val)

    def inverse(operation):
        match operation:
            case "+":
                return "-"
            case "-":
                return "+"
            case "*":
                return "/"
            case "/":
                return "*"

    def equation_side_has_humn(e):
        if e == "humn":
            return True
        elif type(e) != tuple:
            return False
        
        return equation_side_has_humn(e[0]) or equation_side_has_humn(e[2])

    for line in puzzle_input:
        Monkey(line)

    equation_left, _, equation_right = Monkey.monkeys["root"].to_equation()
    if type(equation_left) != tuple:
        equation_left, equation_right = equation_right, equation_left
    if not equation_side_has_humn(equation_left[0]) and equation_left[1] in "+*":
        equation_left = equation_left[::-1]

    while True:
        match equation_left:
            case "humn":
                break
            case (left_val, "-", right_val):
                equation_left = left_val
                equation_right = (right_val, "+", equation_right)
            case (left_val, "/", right_val):
                equation_left = left_val
                equation_right = (right_val, "*", equation_right)
            case (left_val, operation, right_val):
                equation_left = left_val
                equation_right = (equation_right, inverse(operation), right_val)

        if not equation_side_has_humn(equation_left):
            equation_left, equation_right = equation_right, equation_left
        if not equation_side_has_humn(equation_left[0]) and equation_left[1] in "+*":
            equation_left = equation_left[::-1]

        match equation_right:
            case (right_left_val, "+", right_right_val):
                equation_right = right_left_val + right_right_val
            case (right_left_val, "-", right_right_val):
                equation_right = right_left_val - right_right_val
            case (right_left_val, "*", right_right_val):
                equation_right = right_left_val * right_right_val
            case (right_left_val, "/", right_right_val):
                equation_right = right_left_val / right_right_val
                if equation_right == int(equation_right):
                    equation_right = int(equation_right)

    return equation_right

def main():
    puzzle_input = util.read.as_lines()

    root = solve(puzzle_input)

    print("The number that the human will need to yell is " + str(root) + ".")

class AOC_Tests(unittest.TestCase):
    def test_ex1(self):
        return self.assertEqual(solve(["root: pppw + sjmn",
                                       "dbpl: 5",
                                       "cczh: sllz + lgvd",
                                       "zczc: 2",
                                       "ptdq: humn - dvpt",
                                       "dvpt: 3",
                                       "lfqf: 4",
                                       "humn: 5",
                                       "ljgn: 2",
                                       "sjmn: drzm * dbpl",
                                       "sllz: 4",
                                       "pppw: cczh / lfqf",
                                       "lgvd: ljgn * ptdq",
                                       "drzm: hmdt - zczc",
                                       "hmdt: 32"]), 301)

run(main)
