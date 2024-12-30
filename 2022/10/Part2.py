#!/usr/bin/env python3

#Advent of Code
#2022 Day 10, Part 2
#Solution by James C. (https://github.com/JamesMCo)

import os, sys
sys.path.append(os.path.abspath("../.."))
import unittest, util.read
from util.tests import run

from itertools import islice

def solve(puzzle_input):
    class CPU:
        def __init__(self, instructions):
            self.x = 1
            self.instructions = [instruction.split() for instruction in instructions]
            self.cycles = 0

        def run(self):
            self.cycles = 0
            yield self.x
            for instruction in self.instructions:
                match instruction:
                    case ["noop"]:
                        self.cycles += 1
                        yield self.x
                    case ["addx", v]:
                        for c in range(2):
                            self.cycles += 1
                            yield self.x
                        self.x += int(v)
            raise StopIteration

    class Screen:
        def __init__(self, puzzle_input):
            self.cpu = CPU(puzzle_input)
            self.pixels = [["." for pixel in range(40)] for row in range(6)]

        def run(self):
            row = 0
            col = 0
            for x in islice(self.cpu.run(), 1, 241):
                if x - 1 <= col <= x + 1:
                    self.pixels[row][col] = "#"

                if col == 39:
                    row += 1
                    col = 0
                else:
                    col += 1

        def __str__(self):
            return "\n".join(["".join(row) for row in self.pixels])

    screen = Screen(puzzle_input)
    screen.run()
    return str(screen)

def main():
    puzzle_input = util.read.as_lines()

    letters = solve(puzzle_input)

    print("The eight capital letters that appear on the screen are:\n" + str(letters).replace(".", " ").replace("#", "█"))

class AOC_Tests(unittest.TestCase):
    def test_ex1(self):
        return self.assertEqual(solve(["addx 15",  "addx -11", "addx 6",   "addx -3", "addx 5",
                                       "addx -1",  "addx -8",  "addx 13",  "addx 4",  "noop",
                                       "addx -1",  "addx 5",   "addx -1",  "addx 5",  "addx -1",
                                       "addx 5",   "addx -1",  "addx 5",   "addx -1", "addx -35",
                                       "addx 1",   "addx 24",  "addx -19", "addx 1",  "addx 16",
                                       "addx -11", "noop",     "noop",     "addx 21", "addx -15",
                                       "noop",     "noop",     "addx -3",  "addx 9",  "addx 1",
                                       "addx -3",  "addx 8",   "addx 1",   "addx 5",  "noop",
                                       "noop",     "noop",     "noop",     "noop",    "addx -36",
                                       "noop",     "addx 1",   "addx 7",   "noop",    "noop",
                                       "noop",     "addx 2",   "addx 6",   "noop",    "noop",
                                       "noop",     "noop",     "noop",     "addx 1",  "noop",
                                       "noop",     "addx 7",   "addx 1",   "noop",    "addx -13",
                                       "addx 13",  "addx 7",   "noop",     "addx 1",  "addx -33",
                                       "noop",     "noop",     "noop",     "addx 2",  "noop",
                                       "noop",     "noop",     "addx 8",   "noop",    "addx -1",
                                       "addx 2",   "addx 1",   "noop",     "addx 17", "addx -9",
                                       "addx 1",   "addx 1",   "addx -3",  "addx 11", "noop",
                                       "noop",     "addx 1",   "noop",     "addx 1",  "noop",
                                       "noop",     "addx -13", "addx -19", "addx 1",  "addx 3",
                                       "addx 26",  "addx -30", "addx 12",  "addx -1", "addx 3",
                                       "addx 1",   "noop",     "noop",     "noop",    "addx -9",
                                       "addx 18",  "addx 1",   "addx 2",   "noop",    "noop",
                                       "addx 9",   "noop",     "noop",     "noop",    "addx -1",
                                       "addx 2",   "addx -37", "addx 1",   "addx 3",  "noop",
                                       "addx 15",  "addx -21", "addx 22",  "addx -6", "addx 1",
                                       "noop",     "addx 2",   "addx 1",   "noop",    "addx -10",
                                       "noop",     "noop",     "addx 20",  "addx 1",  "addx 2",
                                       "addx 2",   "addx -6",  "addx -11", "noop",    "noop",
                                       "noop"]), 
                                      "##..##..##..##..##..##..##..##..##..##..\n" +
                                      "###...###...###...###...###...###...###.\n" +
                                      "####....####....####....####....####....\n" +
                                      "#####.....#####.....#####.....#####.....\n" +
                                      "######......######......######......####\n" +
                                      "#######.......#######.......#######.....")

if __name__ == "__main__":
    run(main)
