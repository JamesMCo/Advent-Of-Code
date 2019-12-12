#!/usr/bin/env python3

#Advent of Code
#2019 Day 7, Part 2
#Solution by James C. (https://github.com/JamesMCo)

import os, sys
sys.path.append(os.path.abspath("../.."))
import unittest, util.read
from util.tests import run

from colorama import Fore
from itertools import permutations

def solve(puzzle_input):
    class Intcode:
        def __init__(self, code, instream):
            self.opcodes   = {1:  self.add,
                              2:  self.mul,
                              3:  self.inp,
                              4:  self.out,
                              5:  self.jit,
                              6:  self.jif,
                              7:  self.lss,
                              8:  self.eql,
                              99: self.hlt}
            self.instream  = instream
            self.outstream = []

            self.code      = code[:]
            self.ip        = 0
            self.halted    = False

            self.debug     = False

        def step(self):
            if not self.halted and (0 <= self.ip <= len(self.code)):
                op = self.code[self.ip]
                try:
                    self.opcodes[op % 100](op)
                except KeyError:
                    self.halted = True
                    raise NotImplementedError(f"Intcode opcode {op} not understood")

        def read(self, mode, offset):
            value = 0
            if mode == "0":   #Position mode
                value = self.code[self.code[self.ip + offset]]
            elif mode == "1": #Immediate mode
                value = self.code[self.ip + offset]
            else:
                raise NotImplementedError(f"Intcode read mode {mode} not understood")
            return value

        def addr(self, mode, offset):
            value = 0
            if mode == "0":   #Position mode
                value = self.code[self.ip + offset]
            elif mode == "1": #Immediate mode
                raise NotImplementedError(f"Intcode read mode {mode} not supported on output addresses")
            return value

        def add(self, op):
            o = str(op).zfill(5)
            a = self.read(o[2], 1)
            b = self.read(o[1], 2)
            l = self.addr(o[0], 3)

            if self.debug:
                pad = " " * (len(str(self.ip)) + 2)
                print(f"[{Fore.CYAN}{self.ip}{Fore.RESET}] {Fore.YELLOW}{op} {Fore.GREEN}{self.code[self.ip + 1]} {self.code[self.ip + 2]} {self.code[self.ip + 3]}{Fore.RESET}")
                print(f"{pad} - {Fore.YELLOW}ADD{Fore.RESET}")
                if o[2]   == "0":
                    print(f"{pad}   * {Fore.GREEN}{self.code[self.ip + 1]}{Fore.RESET} in position mode (value {a})")
                elif o[2] == "1":
                    print(f"{pad}   * {Fore.GREEN}{self.code[self.ip + 1]}{Fore.RESET} in immediate mode")
                if o[1]   == "0":
                    print(f"{pad}   * {Fore.GREEN}{self.code[self.ip + 2]}{Fore.RESET} in position mode (value {b})")
                elif o[1] == "1":
                    print(f"{pad}   * {Fore.GREEN}{self.code[self.ip + 2]}{Fore.RESET} in immediate mode")
                print(f"{pad}   = {a} + {b} = {a + b}")
                print(f"{pad} - storing in {Fore.GREEN}{self.code[self.ip + 3]}{Fore.RESET} in position mode (value {l})")
            
            self.code[l] = a + b
            self.ip += 4

        def mul(self, op):
            o = str(op).zfill(5)
            a = self.read(o[2], 1)
            b = self.read(o[1], 2)
            l = self.addr(o[0], 3)

            if self.debug:
                pad = " " * (len(str(self.ip)) + 2)
                print(f"[{Fore.CYAN}{self.ip}{Fore.RESET}] {Fore.YELLOW}{op} {Fore.GREEN}{self.code[self.ip + 1]} {self.code[self.ip + 2]} {self.code[self.ip + 3]}{Fore.RESET}")
                print(f"{pad} - {Fore.YELLOW}MUL{Fore.RESET}")
                if o[2]   == "0":
                    print(f"{pad}   * {Fore.GREEN}{self.code[self.ip + 1]}{Fore.RESET} in position mode (value {a})")
                elif o[2] == "1":
                    print(f"{pad}   * {Fore.GREEN}{self.code[self.ip + 1]}{Fore.RESET} in immediate mode")
                if o[1]   == "0":
                    print(f"{pad}   * {Fore.GREEN}{self.code[self.ip + 2]}{Fore.RESET} in position mode (value {b})")
                elif o[1] == "1":
                    print(f"{pad}   * {Fore.GREEN}{self.code[self.ip + 2]}{Fore.RESET} in immediate mode")
                print(f"{pad}   = {a} * {b} = {a * b}")
                print(f"{pad} - storing in {Fore.GREEN}{self.code[self.ip + 3]}{Fore.RESET} in position mode (value {l})")
            
            self.code[l] = a * b
            self.ip += 4

        def inp(self, op):
            o = str(op).zfill(3)
            l = self.addr(o[0], 1)

            if self.debug:
                pad = " " * (len(str(self.ip)) + 2)
                print(f"[{Fore.CYAN}{self.ip}{Fore.RESET}] {Fore.YELLOW}{op} {Fore.GREEN}{self.code[self.ip + 1]}{Fore.RESET}")
                print(f"{pad} - {Fore.YELLOW}INP{Fore.RESET}")
                if len(self.instream) > 0:
                    print(f"{pad}   = {self.instream[0]}")
                    print(f"{pad} - storing in {Fore.GREEN}{self.code[self.ip + 3]}{Fore.RESET} in position mode (value {l})")
                else:
                    print(f"{pad}   = Input stream empty, pausing")
            
            if len(self.instream) > 0:
                self.code[l] = self.instream.pop(0)
                self.ip += 2

        def out(self, op):
            o = str(op).zfill(3)
            v = self.read(o[0], 1)

            if self.debug:
                pad = " " * (len(str(self.ip)) + 2)
                print(f"[{Fore.CYAN}{self.ip}{Fore.RESET}] {Fore.YELLOW}{op} {Fore.GREEN}{self.code[self.ip + 1]}{Fore.RESET}")
                print(f"{pad} - {Fore.YELLOW}OUT{Fore.RESET}")
                if o[0]   == "0":
                    print(f"{pad}   * {Fore.GREEN}{self.code[self.ip + 1]}{Fore.RESET} in position mode (value {v})")
                elif o[0] == "1":
                    print(f"{pad}   * {Fore.GREEN}{self.code[self.ip + 1]}{Fore.RESET} in immediate mode")
                print(f"{pad}   = {v}")

            self.outstream.append(v)
            self.last_out = v
            self.ip += 2

        def jit(self, op):
            o = str(op).zfill(4)
            b = self.read(o[1], 1)
            p = self.read(o[0], 2)

            if self.debug:
                pad = " " * (len(str(self.ip)) + 2)
                print(f"[{Fore.CYAN}{self.ip}{Fore.RESET}] {Fore.YELLOW}{op} {Fore.GREEN}{self.code[self.ip + 1]} {self.code[self.ip + 2]}{Fore.RESET}")
                print(f"{pad} - {Fore.YELLOW}JIT{Fore.RESET}")
                if o[1]   == "0":
                    print(f"{pad}   * {Fore.GREEN}{self.code[self.ip + 1]}{Fore.RESET} in position mode (value {b})")
                elif o[1] == "1":
                    print(f"{pad}   * {Fore.GREEN}{self.code[self.ip + 1]}{Fore.RESET} in immediate mode")
                if o[0]   == "0":
                    print(f"{pad}   * {Fore.GREEN}{self.code[self.ip + 2]}{Fore.RESET} in position mode (value {p})")
                elif o[0] == "1":
                    print(f"{pad}   * {Fore.GREEN}{self.code[self.ip + 2]}{Fore.RESET} in immediate mode")
                if b != 0:
                    print(f"{pad}   = {b} != 0, jumping to address {p}")
                else:
                    print(f"{pad}   = {b} == 0, not jumping")

            if b != 0:
                self.ip = p
            else:
                self.ip += 3

        def jif(self, op):
            o = str(op).zfill(4)
            b = self.read(o[1], 1)
            p = self.read(o[0], 2)

            if self.debug:
                pad = " " * (len(str(self.ip)) + 2)
                print(f"[{Fore.CYAN}{self.ip}{Fore.RESET}] {Fore.YELLOW}{op} {Fore.GREEN}{self.code[self.ip + 1]} {self.code[self.ip + 2]}{Fore.RESET}")
                print(f"{pad} - {Fore.YELLOW}JIF{Fore.RESET}")
                if o[1]   == "0":
                    print(f"{pad}   * {Fore.GREEN}{self.code[self.ip + 1]}{Fore.RESET} in position mode (value {b})")
                elif o[1] == "1":
                    print(f"{pad}   * {Fore.GREEN}{self.code[self.ip + 1]}{Fore.RESET} in immediate mode")
                if o[0]   == "0":
                    print(f"{pad}   * {Fore.GREEN}{self.code[self.ip + 2]}{Fore.RESET} in position mode (value {p})")
                elif o[0] == "1":
                    print(f"{pad}   * {Fore.GREEN}{self.code[self.ip + 2]}{Fore.RESET} in immediate mode")
                if b == 0:
                    print(f"{pad}   = {b} == 0, jumping to address {p}")
                else:
                    print(f"{pad}   = {b} != 0, not jumping")

            if b == 0:
                self.ip = p
            else:
                self.ip += 3

        def lss(self, op):
            o = str(op).zfill(5)
            a = self.read(o[2], 1)
            b = self.read(o[1], 2)
            l = self.addr(o[0], 3)

            if self.debug:
                pad = " " * (len(str(self.ip)) + 2)
                print(f"[{Fore.CYAN}{self.ip}{Fore.RESET}] {Fore.YELLOW}{op} {Fore.GREEN}{self.code[self.ip + 1]} {self.code[self.ip + 2]}{Fore.RESET}")
                print(f"{pad} - {Fore.YELLOW}LSS{Fore.RESET}")
                if o[2]   == "0":
                    print(f"{pad}   * {Fore.GREEN}{self.code[self.ip + 1]}{Fore.RESET} in position mode (value {a})")
                elif o[2] == "1":
                    print(f"{pad}   * {Fore.GREEN}{self.code[self.ip + 1]}{Fore.RESET} in immediate mode")
                if o[1]   == "0":
                    print(f"{pad}   * {Fore.GREEN}{self.code[self.ip + 2]}{Fore.RESET} in position mode (value {b})")
                elif o[1] == "1":
                    print(f"{pad}   * {Fore.GREEN}{self.code[self.ip + 2]}{Fore.RESET} in immediate mode")
                if a < b:
                    print(f"{pad}   = {a} < {b}, result 1")
                else:
                    print(f"{pad}   = {a} !< {b}, result 0")
                print(f"{pad} - storing in {Fore.GREEN}{self.code[self.ip + 3]}{Fore.RESET} in position mode (value {l})")

            if a < b:
                self.code[l] = 1
            else:
                self.code[l] = 0
            self.ip += 4

        def eql(self, op):
            o = str(op).zfill(5)
            a = self.read(o[2], 1)
            b = self.read(o[1], 2)
            l = self.addr(o[0], 3)

            if self.debug:
                pad = " " * (len(str(self.ip)) + 2)
                print(f"[{Fore.CYAN}{self.ip}{Fore.RESET}] {Fore.YELLOW}{op} {Fore.GREEN}{self.code[self.ip + 1]} {self.code[self.ip + 2]}{Fore.RESET}")
                print(f"{pad} - {Fore.YELLOW}EQL{Fore.RESET}")
                if o[2]   == "0":
                    print(f"{pad}   * {Fore.GREEN}{self.code[self.ip + 1]}{Fore.RESET} in position mode (value {a})")
                elif o[2] == "1":
                    print(f"{pad}   * {Fore.GREEN}{self.code[self.ip + 1]}{Fore.RESET} in immediate mode")
                if o[1]   == "0":
                    print(f"{pad}   * {Fore.GREEN}{self.code[self.ip + 2]}{Fore.RESET} in position mode (value {b})")
                elif o[1] == "1":
                    print(f"{pad}   * {Fore.GREEN}{self.code[self.ip + 2]}{Fore.RESET} in immediate mode")
                if a < b:
                    print(f"{pad}   = {a} == {b}, result 1")
                else:
                    print(f"{pad}   = {a} != {b}, result 0")
                print(f"{pad} - storing in {Fore.GREEN}{self.code[self.ip + 3]}{Fore.RESET} in relative mode (value {l})")

            if a == b:
                self.code[l] = 1
            else:
                self.code[l] = 0
            self.ip += 4

        def hlt(self, op):
            if self.debug:
                pad = " " * (len(str(self.ip)) + 2)
                print(f"[{Fore.CYAN}{self.ip}{Fore.RESET}] {Fore.YELLOW}{op}{Fore.RESET}")
                print(f"{pad} - {Fore.YELLOW}HLT{Fore.RESET}")

            self.halted = True

    def try_sequence(seq):
        amps = [Intcode(puzzle_input, [phase]) for phase in seq]
        amps[0].instream.append(0)

        while not all(a.halted for a in amps):
            amps[0].step()
            if len(amps[0].outstream) == 1:
                amps[1].instream.append(amps[0].outstream.pop())

            amps[1].step()
            if len(amps[1].outstream) == 1:
                amps[2].instream.append(amps[1].outstream.pop())

            amps[2].step()
            if len(amps[2].outstream) == 1:
                amps[3].instream.append(amps[2].outstream.pop())

            amps[3].step()
            if len(amps[3].outstream) == 1:
                amps[4].instream.append(amps[3].outstream.pop())

            amps[4].step()
            if len(amps[4].outstream) == 1:
                amps[0].instream.append(amps[4].outstream.pop())

        return amps[4].last_out

    return max(try_sequence(x) for x in permutations([5, 6, 7, 8, 9]))

def main():
    puzzle_input = util.read.as_int_list(",")

    signal = solve(puzzle_input)

    print("The highest signal that can be sent to the thrusters is " + str(signal) + ".")

class AOC_Tests(unittest.TestCase):
    def test_ex1(self):
        self.assertEqual(solve([3,  26, 1001,   26, -4, 26,  3,   27, 1002, 27,  2, 27, 1, 27, 26,
                                27,  4,   27, 1001, 28, -1, 28, 1005,   28,  6, 99,  0, 0,  5]), 139629729)

    def test_ex2(self):
        self.assertEqual(solve([ 3,   52, 1001, 52, -5,   52,  3, 53,  1,   52, 56, 54, 1007,   54,  5, 55, 1005, 55, 26, 1001, 54,
                                -5,   54, 1105,  1, 12,    1, 53, 54, 53, 1008, 54,  0,   55, 1001, 55,  1,   55,  2, 53,   55, 53, 4,
                                53, 1001,   56, -1, 56, 1005, 56,  6, 99,    0,  0,  0,    0,   10]), 18216)

run(main)
