#!/usr/bin/env python3

#Advent of Code
#2020 Day 8, Part 1
#Solution by James C. (https://github.com/JamesMCo)

import os, sys
sys.path.append(os.path.abspath("../.."))
import unittest, util.read
from util.tests import run

def solve(puzzle_input):
    class HGC:
        def __init__(self, program):
            self.program = program
            self.bounds  = len(program)

            self.acc = 0
            self.ip  = 0
            
            self.seen = set()

        def run(self):
            while self.ip not in self.seen:
                self.seen.add(self.ip)
                self.execute(*self.program[self.ip])

        def execute(self, op, arg):
            if op == "acc":
                self.acc += arg
                self.ip += 1
            elif op == "jmp":
                self.ip += arg
            elif op == "nop":
                self.ip += 1

    console = HGC([(line.split()[0], int(line.split()[1])) for line in puzzle_input])
    console.run()
    return console.acc

def main():
    puzzle_input = util.read.as_lines()

    acc = solve(puzzle_input)

    print("The value in the accumulator before an instruction is executed for a second time is " + str(acc) + ".")

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
                                       "acc +6"]), 5)

if __name__ == "__main__":
    run(main)
