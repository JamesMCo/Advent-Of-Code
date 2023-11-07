#!/usr/bin/env python3

#Advent of Code
#2019 Day 13, Part 2
#Solution by James C. (https://github.com/JamesMCo)

import os, sys
sys.path.append(os.path.abspath("../.."))
import unittest, util.read
from util.tests import run

from itertools import batched
from util.two_d_world import World
from util.intcode_2019 import Instruction, IntcodeComputer

def solve(puzzle_input):
    i = IntcodeComputer().load_memory(puzzle_input)
    i.memory[0] = 2

    display = World(0, True)

    score    = None
    paddle_x = None
    ball_x   = None

    while not i.halted:
        if Instruction.get(i, i.instruction_pointer).name == "INP":
            for x, y, tile in batched(i.outputs, 3):
                if (x, y) == (-1, 0):
                    score = tile
                else:
                    display[(x, y)] = tile
                    if tile == 3:
                        paddle_x = x
                    elif tile == 4:
                        ball_x = x

                    display.min_x = min(x, display.min_x)
                    display.min_y = min(y, display.min_y)
                    display.max_x = max(x, display.max_x)
                    display.max_y = max(y, display.max_y)

            i.outputs.clear()
            if paddle_x > ball_x:
                i.queue_inputs(-1)
            elif paddle_x == ball_x:
                i.queue_inputs(0)
            else:
                i.queue_inputs(1)
        i.step()

    for x, y, tile in batched(i.outputs, 3):
        if (x, y) == (-1, 0):
            score = tile

    return score

def main():
    puzzle_input = util.read.as_int_list(",")

    score = solve(puzzle_input)

    print("The score after the last block is broken is " + str(score) + ".")

class AOC_Tests(unittest.TestCase):
    @unittest.skip("No test cases")
    def test_ex1(self):
        pass

run(main)
