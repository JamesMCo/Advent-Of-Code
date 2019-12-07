#!/usr/bin/env python3

#Advent of Code
#2019 Day 5, Part 2
#Solution by James C. (https://github.com/JamesMCo)

import os, sys
sys.path.append(os.path.abspath("../.."))
import unittest, util.read
from util.tests import run

from colorama import Fore

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

        def add(self, op):
            o = str(op).zfill(5)
            a = self.read(o[2], 1)
            b = self.read(o[1], 2)
            l = self.read("1",  3)

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
                print(f"{pad} - storing in {Fore.GREEN}{l}{Fore.RESET}")
            
            self.code[l] = a + b
            self.ip += 4

        def mul(self, op):
            o = str(op).zfill(5)
            a = self.read(o[2], 1)
            b = self.read(o[1], 2)
            l = self.read("1",  3)

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
                print(f"{pad} - storing in {Fore.GREEN}{l}{Fore.RESET}")
            
            self.code[l] = a * b
            self.ip += 4

        def inp(self, op):
            o = str(op).zfill(3)
            l = self.read("1",  1)

            if self.debug:
                pad = " " * (len(str(self.ip)) + 2)
                print(f"[{Fore.CYAN}{self.ip}{Fore.RESET}] {Fore.YELLOW}{op} {Fore.GREEN}{self.code[self.ip + 1]}{Fore.RESET}")
                print(f"{pad} - {Fore.YELLOW}INP{Fore.RESET}")
                print(f"{pad}   = 5")
                print(f"{pad} - storing in {Fore.GREEN}{l}{Fore.RESET}")
            
            self.code[l] = 5
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
            l = self.read("1",  3)

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
                print(f"{pad} - storing in {Fore.GREEN}{l}{Fore.RESET}")

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
                print(f"{pad} - storing in {Fore.GREEN}{l}{Fore.RESET}")

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
