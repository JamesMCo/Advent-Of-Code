#!/usr/bin/env python3

#Advent of Code
#2020 Day 14, Part 2
#Solution by James C. (https://github.com/JamesMCo)

import os, sys
sys.path.append(os.path.abspath("../.."))
import unittest, util.read
from util.tests import run

import re

def solve(puzzle_input):
    memory = {}
    p_mask = re.compile(r"mask = ([X10]{36})")
    p_set  = re.compile(r"mem\[(\d+)] = (\d+)")

    for line in puzzle_input:
        if (m := re.match(p_mask, line)):
            mask = m.group(1)
        else:
            m = re.match(p_set, line)
            addr = list(bin(int(m.group(1)))[2:].zfill(36))
            val  = int(m.group(2))
            
            floating_indexes = []
            for i in range(36):
                if mask[i] == "1":
                    addr[i] = "1"
                elif mask[i] == "X":
                    floating_indexes.append(i)
            floating_count = len(floating_indexes)
            
            for bits in range(2**floating_count):
                floating_vals = bin(bits)[2:].zfill(floating_count)
                for i, v in zip(floating_indexes, floating_vals):
                    addr[i] = v
                memory[int("".join(addr), 2)] = val

    return sum(memory.values())

def main():
    puzzle_input = util.read.as_lines()

    values = solve(puzzle_input)

    print("The sum of all values left in memory is " + str(values) + ".")

class AOC_Tests(unittest.TestCase):
    def test_ex1(self):
        return self.assertEqual(solve(["mask = 000000000000000000000000000000X1001X",
                                       "mem[42] = 100",
                                       "mask = 00000000000000000000000000000000X0XX",
                                       "mem[26] = 1"]), 208)

run(main)
