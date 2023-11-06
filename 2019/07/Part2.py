#!/usr/bin/env python3

#Advent of Code
#2019 Day 7, Part 2
#Solution by James C. (https://github.com/JamesMCo)

import os, sys
sys.path.append(os.path.abspath("../.."))
import unittest, util.read
from util.tests import run

from itertools import permutations
from util.intcode_2019 import IntcodeComputer

def solve(puzzle_input):
    amps = [IntcodeComputer().load_memory(puzzle_input) for i in range(5)]
    for early, late in zip(amps, amps[1:] + [amps[0]]):
        early.register_output_listener(late.queue_inputs)

    def try_sequence(seq):
        for amp, phase in zip(amps, seq):
            amp.reset().queue_inputs(phase)
        amps[0].queue_inputs(0)

        while any(not amp.halted for amp in amps):
            for amp in amps:
                amp.step()

        return amps[-1].outputs[-1]

    return max(try_sequence(x) for x in permutations([5, 6, 7, 8, 9]))

def main():
    puzzle_input = util.read.as_int_list(",")

    signal = solve(puzzle_input)

    print("The highest signal that can be sent to the thrusters is " + str(signal) + ".")

class AOC_Tests(unittest.TestCase):
    def test_ex1(self):
        self.assertEqual(solve([3,  26, 1001,   26, -4, 26,  3,   27, 1002, 27,  2, 27, 1, 27, 26,
                                27,  4,   27, 1001, 28, -1, 28, 1005,   28,  6, 99,  0, 0,  5]), 139629729)

    def test_ex2(self):
        self.assertEqual(solve([ 3,   52, 1001, 52, -5,   52,  3, 53,  1,   52, 56, 54, 1007,   54,  5, 55, 1005, 55, 26, 1001, 54,
                                -5,   54, 1105,  1, 12,    1, 53, 54, 53, 1008, 54,  0,   55, 1001, 55,  1,   55,  2, 53,   55, 53, 4,
                                53, 1001,   56, -1, 56, 1005, 56,  6, 99,    0,  0,  0,    0,   10]), 18216)

run(main)
