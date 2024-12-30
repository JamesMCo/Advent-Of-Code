#!/usr/bin/env python3

#Advent of Code
#2020 Day 14, Part 1
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
            addr = int(m.group(1))
            val  = list(bin(int(m.group(2)))[2:].zfill(36))
            
            for i in range(36):
                if mask[i] != "X":
                    val[i] = mask[i]

            memory[addr] = int("".join(val), 2)

    return sum(memory.values())

def main():
    puzzle_input = util.read.as_lines()

    values = solve(puzzle_input)

    print("The sum of all values left in memory is " + str(values) + ".")

class AOC_Tests(unittest.TestCase):
    def test_ex1(self):
        return self.assertEqual(solve(["mask = XXXXXXXXXXXXXXXXXXXXXXXXXXXXX1XXXX0X",
                                       "mem[8] = 11",
                                       "mem[7] = 101",
                                       "mem[8] = 0"]), 165)

if __name__ == "__main__":
    run(main)
