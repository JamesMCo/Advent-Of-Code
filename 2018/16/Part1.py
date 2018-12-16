#!/usr/bin/env python3

#Advent of Code
#2018 Day 16, Part 1
#Solution by James C. (https://github.com/JamesMCo)

import os, sys
sys.path.append(os.path.abspath("../.."))
import unittest, util.read
from util.tests import run

def solve(puzzle_input):
    class ALU:
        def __init__(self):
            self.register = [0, 0, 0, 0]

        def test(self, initial, instruction, result):
            a, b, c = [int(x) for x in instruction.split()[1:]]
            matches = 0
            for i in [self.addr, self.addi, self.mulr, self.muli,
                      self.banr, self.bani, self.borr, self.bori,
                      self.setr, self.seti, self.gtir, self.gtri,
                      self.gtrr, self.eqir, self.eqri, self.eqrr]:
                self.register = initial[:]
                i(a, b, c)
                if self.register == result:
                    matches += 1
            return matches


        def addr(self, a, b, c):
            self.register[c] = self.register[a] + self.register[b]

        def addi(self, a, b, c):
            self.register[c] = self.register[a] + b

        def mulr(self, a, b, c):
            self.register[c] = self.register[a] * self.register[b]

        def muli(self, a, b, c):
            self.register[c] = self.register[a] * b

        def banr(self, a, b, c):
            self.register[c] = self.register[a] & self.register[b]

        def bani(self, a, b, c):
            self.register[c] = self.register[a] & b

        def borr(self, a, b, c):
            self.register[c] = self.register[a] | self.register[b]

        def bori(self, a, b, c):
            self.register[c] = self.register[a] | b

        def setr(self, a, b, c):
            self.register[c] = self.register[a]

        def seti(self, a, b, c):
            self.register[c] = a

        def gtir(self, a, b, c):
            if a > self.register[b]:
                self.register[c] = 1
            else:
                self.register[c] = 0

        def gtri(self, a, b, c):
            if self.register[a] > b:
                self.register[c] = 1
            else:
                self.register[c] = 0

        def gtrr(self, a, b, c):
            if self.register[a] > self.register[b]:
                self.register[c] = 1
            else:
                self.register[c] = 0

        def eqir(self, a, b, c):
            if a == self.register[b]:
                self.register[c] = 1
            else:
                self.register[c] = 0

        def eqri(self, a, b, c):
            if self.register[a] == b:
                self.register[c] = 1
            else:
                self.register[c] = 0

        def eqrr(self, a, b, c):
            if self.register[a] == self.register[b]:
                self.register[c] = 1
            else:
                self.register[c] = 0

    samples = 0
    alu = ALU()
    while len(puzzle_input) > 0 and "Before:" in puzzle_input[0]:
        initial_state = eval(puzzle_input[0].split("Before: ")[1])
        result_state  = eval(puzzle_input[2].split("After:  ")[1])
        if alu.test(initial_state, puzzle_input[1], result_state) >= 3:
            samples += 1
        puzzle_input = puzzle_input[4:]
    return samples

def main():
    puzzle_input = util.read.as_lines()

    samples = solve(puzzle_input)

    print("The number of samples that behave like three or more opcodes is " + str(samples) + ".")

class AOC_Tests(unittest.TestCase):
    def test_ex1(self):
        self.assertEqual(solve(["Before: [3, 2, 1, 1]",
                                "9 2 1 2",
                                "After:  [3, 2, 2, 1]"]), 1)

run(main)
