#!/usr/bin/env python3

#Advent of Code
#2016 Day 25, Part 1
#Solution by James C. (https://github.com/JamesMCo)

import os, sys
sys.path.append(os.path.abspath("../.."))
import unittest, util.read
from util.tests import run

def solve(puzzle_input):
    lowest = 0
    breakout = False

    while not breakout:
        registers = {"a": lowest}
        output = ""

        # print("New run: a initialised to " + str(registers["a"]))

        i = 0
        k = 0
        while i < len(puzzle_input) and k < 20 and not breakout:
            j = puzzle_input[i].split(" ")
            if j[0] == "cpy":
                try:
                    int(j[1])
                    registers[j[2]] = int(j[1])
                except:
                    registers[j[2]] = registers[j[1]]
            elif j[0] == "inc":
                registers[j[1]] += 1
            elif j[0] == "dec":
                registers[j[1]] -= 1
            elif j[0] == "jnz":
                try:
                    int(j[1])
                    if j[1] != "0":
                        try:
                            int(j[2])
                            i += int(j[2]) - 1
                        except:
                            i += registers[j[2]] - 1
                except:
                    if j[1] in registers and registers[j[1]] != 0 and j[2] != 0:
                        i += int(j[2]) - 1
            elif j[0] == "out":
                try:
                    int(j[1])
                    # print(int(j[1]), end="")
                    output += str(int(j[1]))
                except:
                    # print(registers[j[1]], end="")
                    output += str(registers[j[1]])
                if output[-15:] == "101010101010101" or output[-15:] == "010101010101010":
                    breakout = True
                k += 1
            i += 1

        # print("\n")
        if not breakout:
            lowest += 1

    return lowest


def main():
    puzzle_input = util.read.as_lines()

    lowest = solve(puzzle_input)

    print("The lowest initialisation of register a that causes a clock is " + str(lowest) + ".")

class AOC_Tests(unittest.TestCase):
    @unittest.skip("No test cases")
    def test_ex1(self):
        pass

run(main)
