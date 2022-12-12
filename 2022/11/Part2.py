#!/usr/bin/env python3

#Advent of Code
#2022 Day 11, Part 2
#Solution by James C. (https://github.com/JamesMCo)

import os, sys
sys.path.append(os.path.abspath("../.."))
import unittest, util.read
from util.tests import run

import math
import re

def solve(puzzle_input):
    class Item:
        def __init__(self, value, modulos):
            self.modulos = modulos
            self.values  = {}
            
            for modulo in self.modulos:
                self.values[modulo] = value % modulo

        def __add__(self, other):
            if isinstance(other, int):
                for modulo in self.modulos:
                    self.values[modulo] = (self.values[modulo] + other) % modulo
            else:
                for modulo in self.modulos:
                    self.values[modulo] = (self.values[modulo] + other.values[modulo]) % modulo
            return self

        def __mul__(self, other):
            if isinstance(other, int):
                for modulo in self.modulos:
                    self.values[modulo] = (self.values[modulo] * other) % modulo
            else:
                for modulo in self.modulos:
                    self.values[modulo] = (self.values[modulo] * other.values[modulo]) % modulo
            return self

    class Operation:
        def __init__(self, description):
            self.left, self.operation, self.right = description.split()
            
            if self.left != "old":
                self.left = int(self.left)
            if self.right != "old":
                self.right = int(self.right)

        def __call__(self, old):
            left  = old if self.left  == "old" else self.left
            right = old if self.right == "old" else self.right
            match self.operation:
                case "+":
                    return left + right
                case "*":
                    return left * right

    class Monkey:
        def __init__(self, description):
            self.id              = int(re.match("Monkey (\d+):", description[0]).groups()[0])
            self.items           = [int(x) for x in description[1].split(": ")[1].split(", ")]
            self.operation       = Operation(re.match("  Operation: new = (.*)", description[2]).groups()[0])
            self.test            = int(re.match("  Test: divisible by (\d+)", description[3]).groups()[0])
            self.true_target_id  = int(re.match("    If true: throw to monkey (\d+)", description[4]).groups()[0])
            self.false_target_id = int(re.match("    If false: throw to monkey (\d+)", description[5]).groups()[0])

            self.inspections     = 0

        def register_targets(self, monkeys):
            self.true_target  = monkeys[self.true_target_id]
            self.false_target = monkeys[self.false_target_id]

        def register_items(self, modulos):
            self.items = [Item(value, modulos) for value in self.items]

        def turn(self):
            while self.items:
                current_item = self.items.pop(0)
                self.inspections += 1
                current_item = self.operation(current_item)

                if current_item.values[self.test] == 0:
                    self.true_target.items.append(current_item)
                else:
                    self.false_target.items.append(current_item)

    monkeys = [Monkey(puzzle_input[i:i+6]) for i in range(0, len(puzzle_input), 7)]
    modulos = [monkey.test for monkey in monkeys]
    for monkey in monkeys:
        monkey.register_targets(monkeys)
        monkey.register_items(modulos)

    for throw_round in range(10000):
        for monkey in monkeys:
            monkey.turn()

    return math.prod(sorted(monkey.inspections for monkey in monkeys)[-2:])

def main():
    puzzle_input = util.read.as_lines()

    monkey_business = solve(puzzle_input)

    print("The level of monkey business after 10000 rounds is " + str(monkey_business) + ".")

class AOC_Tests(unittest.TestCase):
    def test_ex1(self):
        return self.assertEqual(solve(["Monkey 0:",
                                       "  Starting items: 79, 98",
                                       "  Operation: new = old * 19",
                                       "  Test: divisible by 23",
                                       "    If true: throw to monkey 2",
                                       "    If false: throw to monkey 3",
                                       "",
                                       "Monkey 1:",
                                       "  Starting items: 54, 65, 75, 74",
                                       "  Operation: new = old + 6",
                                       "  Test: divisible by 19",
                                       "    If true: throw to monkey 2",
                                       "    If false: throw to monkey 0",
                                       "",
                                       "Monkey 2:",
                                       "  Starting items: 79, 60, 97",
                                       "  Operation: new = old * old",
                                       "  Test: divisible by 13",
                                       "    If true: throw to monkey 1",
                                       "    If false: throw to monkey 3",
                                       "",
                                       "Monkey 3:",
                                       "  Starting items: 74",
                                       "  Operation: new = old + 3",
                                       "  Test: divisible by 17",
                                       "    If true: throw to monkey 0",
                                       "    If false: throw to monkey 1"]), 2713310158)

run(main)
