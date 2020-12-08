#!/usr/bin/env python3

#Advent of Code
#2020 Day 8, Part 2
#Solution by James C. (https://github.com/JamesMCo)

import os, sys
sys.path.append(os.path.abspath("../.."))
import unittest, util.read
from util.tests import run

def solve(puzzle_input):
    class HGC:
        def __init__(self, program, patch_location):
            self.program        = program
            self.bounds         = len(program)
            self.patch_location = patch_location

            self.acc = 0
            self.ip  = 0

        def run(self):
            seen = set()
            while self.ip not in seen and 0 <= self.ip < self.bounds:
                seen.add(self.ip)
                if self.ip == self.patch_location:
                    if self.program[self.ip][0] == "jmp":
                        self.execute("nop", self.program[self.ip][1])
                    else:
                        self.execute("jmp", self.program[self.ip][1])
                else:
                    self.execute(*self.program[self.ip])
            return not (0 <= self.ip < self.bounds)

        def execute(self, op, arg):
            if op == "acc":
                self.acc += arg
                self.ip += 1
            elif op == "jmp":
                self.ip += arg
            elif op == "nop":
                self.ip += 1

    program = [(line.split()[0], int(line.split()[1])) for line in puzzle_input]
    for i in range(len(program)):
        if program[i][0] == "acc": continue
        console = HGC(program, i)
        if console.run():
            return console.acc

def main():
    puzzle_input = util.read.as_lines()

    acc = solve(puzzle_input)

    print("The value in the accumulator after the program terminates is " + str(acc) + ".")

class AOC_Tests(unittest.TestCase):
    def test_ex1(self):
        return self.assertEqual(solve(["nop +0",
                                       "acc +1",
                                       "jmp +4",
                                       "acc +3",
                                       "jmp -3",
                                       "acc -99",
                                       "acc +1",
                                       "jmp -4",
                                       "acc +6"]), 8)

run(main)
