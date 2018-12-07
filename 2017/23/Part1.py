#!/usr/bin/env python3

#Advent of Code
#Day 23, Part 1
#Solution by James C. (https://github.com/JamesMCo)

import os, sys
sys.path.append(os.path.abspath("../.."))
import unittest
from util.tests import run

import string

def solve(puzzle_input):
    i = 0
    mul_count = 0
    registers = [0 for x in range(8)]

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
        
        
        if op == "set":
            registers[reg]  = val
        elif op == "sub":
            registers[reg] -= val
        elif op == "mul":
            registers[reg] *= val
            mul_count += 1
        elif op == "jnz":
            if reg_num:
                if reg != 0:
                    i += val
                    continue
            else:
                if registers[reg] != 0:
                    i += val
                    continue
        i += 1

    return mul_count

def main():
    f = open("puzzle_input.txt")
    puzzle_input = f.read()[:-1].split("\n")
    f.close()

    muls = solve(puzzle_input)

    print("The mul instruction is invoked " + str(muls) + " times.")

class AOC_Tests(unittest.TestCase):
    def test_ex1(self):
        self.assertEqual(solve(["mul a 1",
                                "mul a 1",
                                "mul a 1"]), 3)

run(main)
