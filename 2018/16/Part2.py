#!/usr/bin/env python3

#Advent of Code
#2018 Day 16, Part 2
#Solution by James C. (https://github.com/JamesMCo)

import os, sys
sys.path.append(os.path.abspath("../.."))
import unittest, util.read
from util.tests import run

import random

def solve(puzzle_input):
    class ALU:
        def __init__(self):
            self.register = [0, 0, 0, 0]
            self.found = [None for i in range(16)]
            self.instruction_map = [None for i in range(16)]

        def test(self, initial, instruction, result):
            a, b, c = [int(x) for x in instruction.split()[1:]]
            matches = []
            for i, x in enumerate([self.addr, self.addi, self.mulr, self.muli,
                                   self.banr, self.bani, self.borr, self.bori,
                                   self.setr, self.seti, self.gtir, self.gtri,
                                   self.gtrr, self.eqir, self.eqri, self.eqrr]):
                self.register = initial[:]
                x(a, b, c)
                if self.register == result:
                    matches.append(i)
            return matches

        def run(self, instruction):
            opcode, a, b, c = [int(x) for x in instruction.split()]
            [self.addr, self.addi, self.mulr, self.muli,
             self.banr, self.bani, self.borr, self.bori,
             self.setr, self.seti, self.gtir, self.gtri,
             self.gtrr, self.eqir, self.eqri, self.eqrr][self.instruction_map[opcode]](a, b, c)


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

    alu = ALU()
    samples = []
    while "Before:" in puzzle_input[0]:
        samples.extend(puzzle_input[:4])
        puzzle_input = puzzle_input[4:]

    full_samples = samples[:]
    loop = len(samples)
    i = 0
    make_a_guess = False
    while len(samples) > 0 and alu.found.count(None) > 0:
        initial_state = eval(samples[0].split("Before: ")[1])
        result_state  = eval(samples[2].split("After:  ")[1])
        matches = alu.test(initial_state, samples[1], result_state)
        matches = [x for x in matches if alu.found[x] == None]
        if len(matches) == 1:
            alu.found[matches[0]] = int(samples[1].split()[0])
            loop -= 1
        else:
            samples.extend(samples[:4])
        samples = samples[4:]

    for i in range(16):
        alu.instruction_map[alu.found[i]] = i

    while puzzle_input[0] == "":
        puzzle_input.pop(0)

    alu.register = [0, 0, 0, 0]
    while len(puzzle_input) > 0:
        alu.run(puzzle_input[0])
        puzzle_input.pop(0)

    return alu.register[0]

def main():
    puzzle_input = util.read.as_lines()

    value = solve(puzzle_input)

    print("The value contained in register 0 after executing the test program is " + str(value) + ".")

class AOC_Tests(unittest.TestCase):
    @unittest.skip("No test cases")
    def test_ex1(self):
        pass

if __name__ == "__main__":
    run(main)
