#!/usr/bin/env python3

#Advent of Code
#2019 Day 5, Part 2
#Solution by James C. (https://github.com/JamesMCo)

import os, sys
sys.path.append(os.path.abspath("../.."))
import unittest, util.read
from util.tests import run

def solve(puzzle_input):
    class Intcode:
        def __init__(self, code):
            self.opcodes   = {1:  self.add,
                              2:  self.mul,
                              3:  self.inp,
                              4:  self.out,
                              5:  self.jit,
                              6:  self.jif,
                              7:  self.lss,
                              8:  self.eql,
                              99: self.hlt}
            self.outstream = []

            self.code      = code
            self.ip        = 0
            self.halted    = False

        def step(self):
            if not self.halted and (0 <= self.ip <= len(self.code)):
                op = self.code[self.ip]
                self.opcodes[op % 100](op)

        def read(self, mode, offset):
            value = 0
            if mode == "0":   #Position mode
                value = self.code[self.code[self.ip + offset]]
            elif mode == "1": #Immediate mode
                value = self.code[self.ip + offset]
            else:
                raise NotImplementedError(f"Intcode read mode {mode} not understood")
            return value

        def add(self, op):
            o = str(op).zfill(5)
            a = self.read(o[2], 1)
            b = self.read(o[1], 2)
            l = self.read("1",  3)
            self.code[l] = a + b
            self.ip += 4

        def mul(self, op):
            o = str(op).zfill(5)
            a = self.read(o[2], 1)
            b = self.read(o[1], 2)
            l = self.read("1",  3)
            self.code[l] = a * b
            self.ip += 4

        def inp(self, op):
            o = str(op).zfill(3)
            l = self.read("1",  1)
            self.code[l] = 5
            self.ip += 2

        def out(self, op):
            o = str(op).zfill(3)
            v = self.read(o[0], 1)
            self.outstream.append(v)
            self.ip += 2

        def jit(self, op):
            o = str(op).zfill(4)
            b = self.read(o[1], 1)
            p = self.read(o[0], 2)
            if b != 0:
                self.ip = p
            else:
                self.ip += 3

        def jif(self, op):
            o = str(op).zfill(4)
            b = self.read(o[1], 1)
            p = self.read(o[0], 2)
            if b == 0:
                self.ip = p
            else:
                self.ip += 3

        def lss(self, op):
            o = str(op).zfill(5)
            a = self.read(o[2], 1)
            b = self.read(o[1], 2)
            l = self.read("1",  3)
            if a < b:
                self.code[l] = 1
            else:
                self.code[l] = 0
            self.ip += 4

        def eql(self, op):
            o = str(op).zfill(5)
            a = self.read(o[2], 1)
            b = self.read(o[1], 2)
            l = self.read("1",  3)
            if a == b:
                self.code[l] = 1
            else:
                self.code[l] = 0
            self.ip += 4

        def hlt(self, op):
            self.halted = True

    i = Intcode(puzzle_input)
    while not i.halted:
        i.step()

    return i.outstream[-1]

def main():
    puzzle_input = util.read.as_int_list(",")

    diag_code = solve(puzzle_input)

    print("The diagnostic code the program produces is " + str(diag_code) + ".")

class AOC_Tests(unittest.TestCase):
    @unittest.skip("No test cases")
    def test_ex1(self):
        pass

run(main)
