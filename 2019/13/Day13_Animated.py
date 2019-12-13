#!/usr/bin/env python3

#Advent of Code
#2019 Day 13, Part 2, Animated
#Solution by James C. (https://github.com/JamesMCo)

import os, sys
sys.path.append(os.path.abspath("../.."))
import util.read

from collections import defaultdict
from math import inf
from time import sleep

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
        self.req_inp   = False

        self.debug     = False

    def step(self):
        self.req_inp = False
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
            if len(self.instream) > 0:
                print(f"{pad}   = {self.instream[0]}")
                print(f"{pad} - storing in {Fore.GREEN}{self.code[self.ip + 3]}{Fore.RESET} in position mode (value {l})")
            else:
                print(f"{pad}   = Input stream empty, requesting")
        
        if len(self.instream) > 0:
            self.code[l] = self.instream.pop(0)
            self.ip += 2
        else:
            self.req_inp = True

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

puzzle_input = util.read.as_int_list(",")
puzzle_input[0] = 2
i = Intcode(puzzle_input, [])

display = defaultdict(int)
min_x   = inf
min_y   = inf
max_x   = -inf
max_y   = -inf

paddle_x = None
ball_x   = None

while not i.halted:
    i.step()
    if i.req_inp:
        for j in range(0, len(i.outstream), 3):
            if i.outstream[j] == -1 and i.outstream[j+1] == 0:
                display["score"] = i.outstream[j+2]
            else:
                display[(i.outstream[j], i.outstream[j+1])] = i.outstream[j+2]
                if i.outstream[j+2] == 3:
                    paddle_x = i.outstream[j]
                elif i.outstream[j+2] == 4:
                    ball_x = i.outstream[j]

                min_x = min(min_x, i.outstream[j])
                min_y = min(min_y, i.outstream[j+1])
                max_x = max(max_x, i.outstream[j])
                max_y = max(max_y, i.outstream[j+1])
        
        os.system("cls" if os.name == "nt" else "clear")
        for y in range(min_y, max_y + 1):
            for x in range(min_x, max_x + 1):
                tile = display[(x, y)]
                if tile   == 0:
                    print(" ", end="")
                elif tile == 1:
                    print("#", end="")
                elif tile == 2:
                    print("+", end="")
                elif tile == 3:
                    print("=", end="")
                elif tile == 4:
                    print("*", end="")
            print()
        print(f"Score: {display['score']}")

        i.outstream = []
        if paddle_x > ball_x:
            i.instream.append(-1)
        elif paddle_x == ball_x:
            i.instream.append(0)
        else:
            i.instream.append(1)

        sleep(0.016)

for j in range(0, len(i.outstream), 3):
    if i.outstream[j] == -1 and i.outstream[j+1] == 0:
        display["score"] = i.outstream[j+2]

print("The number of block tiles on screen when the game exits is " + str(display["score"]) + ".")