#!/usr/bin/env python3

#Advent of Code
#2015 Day 7, Part 1
#Solution by James C. (https://github.com/JamesMCo)

import os, sys
sys.path.append(os.path.abspath("../.."))
import unittest, util.read
from util.tests import run

def solve(puzzle_input):
    def literal(x):
        l = True
        for c in x:
            if c not in "0123456789":
                l = False
                break
        return l

    f = open("puzzle_input.txt")
    puzzle_input = f.read().split("\n")
    f.close()

    wires = {}

    while len(puzzle_input) != 0:
        i = 0
        while i < len(puzzle_input):
            cur = puzzle_input[i]
            ins = cur.split("->")[0].rstrip().split(" ")
            out = cur.split("->")[1].lstrip()
            if len(ins) == 1:
                if literal(ins[0]):
                    wires[out] = int(ins[0])
                    puzzle_input.pop(i)
                elif ins[0] in wires:
                    wires[out] = wires[ins[0]]
                    puzzle_input.pop(i)
                else:
                    i += 1
            else:
                if ins[0] == "NOT":
                    if literal(ins[1]):
                        wires[out] = 65535 - int(ins[1])
                        puzzle_input.pop(i)
                    elif ins[1] in wires:
                        wires[out] = 65535 - wires[ins[1]]
                        puzzle_input.pop(i)
                    else:
                        i += 1
                else:
                    if literal(ins[0]):
                        val1 = int(ins[0])
                    elif ins[0] in wires:
                        val1 = wires[ins[0]]
                    else:
                        i += 1
                        continue
                    if literal(ins[2]):
                        val2 = int(ins[2])
                    elif ins[2] in wires:
                        val2 = wires[ins[2]]
                    else:
                        i += 1
                        continue

                    if ins[1] == "AND":
                        wires[out] = val1 & val2
                        puzzle_input.pop(i)
                    elif ins[1] == "OR":
                        wires[out] = val1 | val2
                        puzzle_input.pop(i)
                    elif ins[1] == "LSHIFT":
                        wires[out] = val1 << val2
                        puzzle_input.pop(i)
                    elif ins[1] == "RSHIFT":
                        wires[out] = val1 >> val2
                        puzzle_input.pop(i)
                    else:
                        i += 1

    return wires["a"]

def main():
    puzzle_input = util.read.as_lines()

    signal = solve(puzzle_input)

    print("The signal provided to wire a is " + str(signal) + "")

class AOC_Tests(unittest.TestCase):
    @unittest.skip("No test cases")
    def test_ex1(self):
        pass

if __name__ == "__main__":
    run(main)
