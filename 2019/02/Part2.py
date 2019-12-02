#!/usr/bin/env python3

#Advent of Code
#2019 Day 2, Part 2
#Solution by James C. (https://github.com/JamesMCo)

import os, sys
sys.path.append(os.path.abspath("../.."))
import unittest, util.read
from util.tests import run

def solve(puzzle_input):
    def run(memory):
        i = 0
        while True:
            opcode = memory[i]
            if opcode == 1:
                memory[memory[i+3]] = memory[memory[i+1]] + memory[memory[i+2]]
                i += 4
            elif opcode == 2:
                memory[memory[i+3]] = memory[memory[i+1]] * memory[memory[i+2]]
                i += 4
            elif opcode == 99:
                return memory

    for noun in range(0, 100):
        for verb in range(0, 100):
            working = puzzle_input[:]
            working[1] = noun
            working[2] = verb

            if run(working)[0] == 19690720:
                return 100 * noun + verb

def main():
    puzzle_input = util.read.as_int_list(",")

    value = solve(puzzle_input)

    print("The value of 100 * noun + verb is " + str(value) + ".")

class AOC_Tests(unittest.TestCase):
    @unittest.skip("No test cases")
    def test_ex1(self):
        pass

run(main)
