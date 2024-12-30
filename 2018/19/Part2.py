#!/usr/bin/env python3

#Advent of Code
#2018 Day 19, Part 2
#Solution by James C. (https://github.com/JamesMCo)

import os, sys
sys.path.append(os.path.abspath("../.."))
import unittest, util.read
from util.tests import run

def solve(puzzle_input):
    class CPU:
        def __init__(self, program):
            self.register = [1, 0, 0, 0, 0, 0]
            self.ip       = 0
            self.ipr      = None
            self.instructions = {"addr": self.addr,
                                 "addi": self.addi,
                                 "mulr": self.mulr,
                                 "muli": self.muli,
                                 "banr": self.banr,
                                 "bani": self.bani,
                                 "borr": self.borr,
                                 "bori": self.bori,
                                 "setr": self.setr,
                                 "seti": self.seti,
                                 "gtir": self.gtir,
                                 "gtri": self.gtri,
                                 "gtrr": self.gtrr,
                                 "eqir": self.eqir,
                                 "eqri": self.eqri,
                                 "eqrr": self.eqrr
                                }
            self.program = program

        def bind_ip(self, r):
            self.ipr = r

        def run(self):
            self.register[self.ipr] = self.ip

            opcode, a, b, c = self.program[self.ip].split()
            self.instructions[opcode](int(a), int(b), int(c))

            self.ip = self.register[self.ipr]
            self.ip += 1


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

    cpu = CPU(puzzle_input[1:])
    cpu.bind_ip(int(puzzle_input[0].split()[1]))
    while 0 <= cpu.ip < len(cpu.program):
        cpu.run()
        if cpu.ip == 1:
            val = max(cpu.register)
            return sum(i for i in range(1, val+1) if val % i == 0)

def main():
    puzzle_input = util.read.as_lines()

    value = solve(puzzle_input)

    print("The value left in register 0 is " + str(value) + ".")

class AOC_Tests(unittest.TestCase):
    @unittest.skip("No test cases")
    def test_ex1(self):
        pass

if __name__ == "__main__":
    run(main)
