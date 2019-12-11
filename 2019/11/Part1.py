#!/usr/bin/env python3

#Advent of Code
#2019 Day 11, Part 1
#Solution by James C. (https://github.com/JamesMCo)

import os, sys
sys.path.append(os.path.abspath("../.."))
import unittest, util.read
from util.tests import run

from collections import defaultdict

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
                              9:  self.arb,
                              99: self.hlt}
            self.instream  = instream
            self.outstream = []

            self.code      = defaultdict(int)
            for ip, instruction in enumerate(code):
                self.code[ip] = instruction

            self.ip        = 0
            self.rel_base  = 0
            self.halted    = False

            self.debug     = False

        def step(self):
            if not self.halted and (0 <= self.ip):
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
            elif mode == "2": #Relative mode
                value = self.code[self.code[self.ip + offset] + self.rel_base]
            else:
                raise NotImplementedError(f"Intcode read mode {mode} not understood")
            return value

        def addr(self, mode, offset):
            value = 0
            if mode == "0":   #Position mode
                value = self.code[self.ip + offset]
            elif mode == "1": #Immediate mode
                raise NotImplementedError(f"Intcode read mode {mode} not supported on output addresses")
            elif mode == "2": #Relative mode
                value = self.code[self.ip + offset] + self.rel_base
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
                elif o[2] == "2":
                    print(f"{pad}   * {Fore.GREEN}{self.code[self.ip + 1]}{Fore.RESET} in relative mode (value {a})")
                if o[1]   == "0":
                    print(f"{pad}   * {Fore.GREEN}{self.code[self.ip + 2]}{Fore.RESET} in position mode (value {b})")
                elif o[1] == "1":
                    print(f"{pad}   * {Fore.GREEN}{self.code[self.ip + 2]}{Fore.RESET} in immediate mode")
                elif o[1] == "2":
                    print(f"{pad}   * {Fore.GREEN}{self.code[self.ip + 2]}{Fore.RESET} in relative mode (value {b})")
                print(f"{pad}   = {a} + {b} = {a + b}")
                if o[0]   == "0":
                    print(f"{pad} - storing in {Fore.GREEN}{self.code[self.ip + 3]}{Fore.RESET} in position mode (value {l})")
                elif o[0] == "2":
                    print(f"{pad} - storing in {Fore.GREEN}{self.code[self.ip + 3]}{Fore.RESET} in relative mode (value {l})")
            
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
                elif o[2] == "2":
                    print(f"{pad}   * {Fore.GREEN}{self.code[self.ip + 1]}{Fore.RESET} in relative mode (value {a})")
                if o[1]   == "0":
                    print(f"{pad}   * {Fore.GREEN}{self.code[self.ip + 2]}{Fore.RESET} in position mode (value {b})")
                elif o[1] == "1":
                    print(f"{pad}   * {Fore.GREEN}{self.code[self.ip + 2]}{Fore.RESET} in immediate mode")
                elif o[1] == "2":
                    print(f"{pad}   * {Fore.GREEN}{self.code[self.ip + 2]}{Fore.RESET} in relative mode (value {b})")
                print(f"{pad}   = {a} * {b} = {a * b}")
                if o[0]   == "0":
                    print(f"{pad} - storing in {Fore.GREEN}{self.code[self.ip + 3]}{Fore.RESET} in position mode (value {l})")
                elif o[0] == "2":
                    print(f"{pad} - storing in {Fore.GREEN}{self.code[self.ip + 3]}{Fore.RESET} in relative mode (value {l})")
            
            self.code[l] = a * b
            self.ip += 4

        def inp(self, op):
            o = str(op).zfill(3)
            l = self.addr(o[0], 1)

            if self.debug:
                pad = " " * (len(str(self.ip)) + 2)
                print(f"[{Fore.CYAN}{self.ip}{Fore.RESET}] {Fore.YELLOW}{op} {Fore.GREEN}{self.code[self.ip + 1]}{Fore.RESET}")
                print(f"{pad} - {Fore.YELLOW}INP{Fore.RESET}")
                print(f"{pad}   = {self.instream[0]}")
                if o[0]   == "0":
                    print(f"{pad} - storing in {Fore.GREEN}{self.code[self.ip + 3]}{Fore.RESET} in position mode (value {l})")
                elif o[0] == "2":
                    print(f"{pad} - storing in {Fore.GREEN}{self.code[self.ip + 3]}{Fore.RESET} in relative mode (value {l})")
            
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
                elif o[0] == "2":
                    print(f"{pad}   * {Fore.GREEN}{self.code[self.ip + 1]}{Fore.RESET} in relative mode (value {v})")
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
                elif o[1] == "2":
                    print(f"{pad}   * {Fore.GREEN}{self.code[self.ip + 1]}{Fore.RESET} in relative mode (value {b})")
                if o[0]   == "0":
                    print(f"{pad}   * {Fore.GREEN}{self.code[self.ip + 2]}{Fore.RESET} in position mode (value {p})")
                elif o[0] == "1":
                    print(f"{pad}   * {Fore.GREEN}{self.code[self.ip + 2]}{Fore.RESET} in immediate mode")
                elif o[0] == "2":
                    print(f"{pad}   * {Fore.GREEN}{self.code[self.ip + 2]}{Fore.RESET} in relative mode (value {p})")
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
                elif o[1] == "2":
                    print(f"{pad}   * {Fore.GREEN}{self.code[self.ip + 1]}{Fore.RESET} in relative mode (value {b})")
                if o[0]   == "0":
                    print(f"{pad}   * {Fore.GREEN}{self.code[self.ip + 2]}{Fore.RESET} in position mode (value {p})")
                elif o[0] == "1":
                    print(f"{pad}   * {Fore.GREEN}{self.code[self.ip + 2]}{Fore.RESET} in immediate mode")
                elif o[0] == "2":
                    print(f"{pad}   * {Fore.GREEN}{self.code[self.ip + 2]}{Fore.RESET} in relative mode (value {p})")
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
                elif o[2] == "2":
                    print(f"{pad}   * {Fore.GREEN}{self.code[self.ip + 1]}{Fore.RESET} in relative mode (value {a})")
                if o[1]   == "0":
                    print(f"{pad}   * {Fore.GREEN}{self.code[self.ip + 2]}{Fore.RESET} in position mode (value {b})")
                elif o[1] == "1":
                    print(f"{pad}   * {Fore.GREEN}{self.code[self.ip + 2]}{Fore.RESET} in immediate mode")
                elif o[1] == "2":
                    print(f"{pad}   * {Fore.GREEN}{self.code[self.ip + 2]}{Fore.RESET} in relative mode (value {b})")
                if a < b:
                    print(f"{pad}   = {a} < {b}, result 1")
                else:
                    print(f"{pad}   = {a} !< {b}, result 0")
                if o[0]   == "0":
                    print(f"{pad} - storing in {Fore.GREEN}{self.code[self.ip + 3]}{Fore.RESET} in position mode (value {l})")
                elif o[0] == "2":
                    print(f"{pad} - storing in {Fore.GREEN}{self.code[self.ip + 3]}{Fore.RESET} in relative mode (value {l})")

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
                elif o[2] == "2":
                    print(f"{pad}   * {Fore.GREEN}{self.code[self.ip + 1]}{Fore.RESET} in relative mode (value {a})")
                if o[1]   == "0":
                    print(f"{pad}   * {Fore.GREEN}{self.code[self.ip + 2]}{Fore.RESET} in position mode (value {b})")
                elif o[1] == "1":
                    print(f"{pad}   * {Fore.GREEN}{self.code[self.ip + 2]}{Fore.RESET} in immediate mode")
                elif o[1] == "2":
                    print(f"{pad}   * {Fore.GREEN}{self.code[self.ip + 2]}{Fore.RESET} in relative mode (value {b})")
                if a < b:
                    print(f"{pad}   = {a} == {b}, result 1")
                else:
                    print(f"{pad}   = {a} != {b}, result 0")
                if o[0]   == "0":
                    print(f"{pad} - storing in {Fore.GREEN}{self.code[self.ip + 3]}{Fore.RESET} in position mode (value {l})")
                elif o[0] == "2":
                    print(f"{pad} - storing in {Fore.GREEN}{self.code[self.ip + 3]}{Fore.RESET} in relative mode (value {l})")

            if a == b:
                self.code[l] = 1
            else:
                self.code[l] = 0
            self.ip += 4

        def arb(self, op):
            o = str(op).zfill(3)
            d = self.read(o[0], 1)

            if self.debug:
                pad = " " * (len(str(self.ip)) + 2)
                print(f"[{Fore.CYAN}{self.ip}{Fore.RESET}] {Fore.YELLOW}{op}{Fore.RESET}")
                print(f"{pad} - {Fore.YELLOW}ARB{Fore.RESET}")
                if o[0]   == "0":
                    print(f"{pad}   * {Fore.GREEN}{self.code[self.ip + 1]}{Fore.RESET} in position mode (value {d})")
                elif o[0] == "1":
                    print(f"{pad}   * {Fore.GREEN}{self.code[self.ip + 1]}{Fore.RESET} in immediate mode")
                elif o[0] == "2":
                    print(f"{pad}   * {Fore.GREEN}{self.code[self.ip + 1]}{Fore.RESET} in relative mode (value {d})")

            self.rel_base += d
            self.ip += 2

        def hlt(self, op):
            if self.debug:
                pad = " " * (len(str(self.ip)) + 2)
                print(f"[{Fore.CYAN}{self.ip}{Fore.RESET}] {Fore.YELLOW}{op}{Fore.RESET}")
                print(f"{pad} - {Fore.YELLOW}HLT{Fore.RESET}")

            self.halted = True

    def walk(robot, current_colour):
        robot.instream.append(current_colour)

        while not robot.halted and len(robot.outstream) != 2:
            robot.step()

        if robot.halted:
            return [0, 0]
        results = robot.outstream[:]
        robot.outstream = []
        return results

    i = Intcode(puzzle_input, [])
    grid = defaultdict(int)
    painted = defaultdict(int)
    x, y = (0, 0)
    direction = "u"

    while not i.halted:
        new_colour, turn = walk(i, grid[(x, y)])
        if i.halted:
            break
        
        grid[(x, y)] = new_colour
        if new_colour == 1:
            painted[(x, y)] = 1

        if turn == 0:
            if direction == "u":
                direction = "l"
            elif direction == "d":
                direction = "r"
            elif direction == "l":
                direction = "d"
            else:
                direction = "u"
        else:
            if direction == "u":
                direction = "r"
            elif direction == "d":
                direction = "l"
            elif direction == "l":
                direction = "u"
            else:
                direction = "d"

        if direction == "u":
            y -= 1
        elif direction == "d":
            y += 1
        elif direction == "l":
            x -= 1
        else:
            x += 1

    return sum(painted.values())

def main():
    puzzle_input = util.read.as_int_list(",")

    panels = solve(puzzle_input)

    print("The number of panels painted at least once is " + str(panels) + ".")

class AOC_Tests(unittest.TestCase):
    @unittest.skip("No test cases")
    def test_ex1(self):
        pass

run(main)
