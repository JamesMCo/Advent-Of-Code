#!/usr/bin/env python3

#Advent of Code
#Day 18, Part 1
#Solution by James C. (https://github.com/JamesMCo)

import os, sys
sys.path.append(os.path.abspath("../.."))
import unittest
from util.tests import run

import string

def solve(puzzle_input):
    i = 0
    last_sound = None
    registers = [0 for x in range(26)]

    while 0 <= i < len(puzzle_input):
        inst        = puzzle_input[i].split()
        op          = inst[0]

        try:
            reg     = int(inst[1])
            reg_num = True
        except:
            reg     = ord(inst[1]) - 97
            reg_num = False

        if len(inst) == 3:
            if inst[2] in string.ascii_lowercase:
                val = registers[ord(inst[2]) - 97]
            else:
                val = int(inst[2])
        else:
            val = None
        
        
        if op == "snd":
            if reg_num:
                last_sound  = reg
            else:
                last_sound  = registers[reg]
        elif op == "set":
            registers[reg]  = val
        elif op == "add":
            registers[reg] += val
        elif op == "mul":
            registers[reg] *= val
        elif op == "mod":
            registers[reg] %= val
        elif op == "rcv":
            if registers[reg] != 0:
                return last_sound
        elif op == "jgz":
            if registers[reg] > 0:
                i += val
                continue
        i += 1

    return None

def main():
    f = open("puzzle_input.txt")
    puzzle_input = f.read()[:-1].split("\n")
    f.close()

    freq = solve(puzzle_input)

    print("The value of the first recovered frequency is " + str(freq) + ".")

class AOC_Tests(unittest.TestCase):
    def test_ex1(self):
        self.assertEqual(solve(["set a 1",
                                "add a 2",
                                "mul a a",
                                "mod a 5",
                                "snd a",
                                "set a 0",
                                "rcv a",
                                "jgz a -1",
                                "set a 1",
                                "jgz a -2"]), 4)

run(main)
