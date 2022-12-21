#!/usr/bin/env python3

#Advent of Code
#2022 Day 21, Part 1
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

            if (match := re.match(Monkey.number_pattern, description)):
                groups = match.groups()
                self.name = groups[0]
                self.val  = int(groups[1])
            elif (match := re.match(Monkey.math_pattern, description)):
                groups = match.groups()
                self.name = groups[0]
                self.dependencies = [groups[1], groups[3]]
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

    for line in puzzle_input:
        Monkey(line)

    return Monkey.monkeys["root"].get_val()

def main():
    puzzle_input = util.read.as_lines()

    root = solve(puzzle_input)

    print("The number that root will yell is " + str(root) + ".")

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
                                       "hmdt: 32"]), 152)

run(main)
