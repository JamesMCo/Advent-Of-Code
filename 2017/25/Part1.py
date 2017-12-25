#!/usr/bin/env python3

#Advent of Code
#Day 25, Part 1
#Solution by James C. (https://github.com/JamesMCo)

import os, sys
sys.path.append(os.path.abspath("../.."))
import unittest, util.tests

import collections

def solve(puzzle_input):
    state = puzzle_input[0].split()[-1][:-1]
    steps = int(puzzle_input[1].split()[-2])
    states = {}
    for i, line in enumerate(puzzle_input):
        if line[:8] == "In state":
            states[line.split()[-1][:-1]] = [
                [
                    int(puzzle_input[i+2].split()[-1][:-1]),
                    int(puzzle_input[i+3].split()[-1][:-1] == "right"),
                    puzzle_input[i+4].split()[-1][:-1]
                ],
                [
                    int(puzzle_input[i+6].split()[-1][:-1]),
                    int(puzzle_input[i+7].split()[-1][:-1] == "right"),
                    puzzle_input[i+8].split()[-1][:-1]
                ]
            ]
            if states[line.split()[-1][:-1]][0][1] == 0:
                states[line.split()[-1][:-1]][0][1] = -1
            if states[line.split()[-1][:-1]][1][1] == 0:
                states[line.split()[-1][:-1]][1][1] = -1
    tape = collections.defaultdict(int)
    pos = 0

    for i in range(steps):
        tape[pos], direction, state = states[state][tape[pos]]
        pos += direction

    return sum(tape.values())

def main():
    f = open("puzzle_input.txt")
    puzzle_input = f.read()[:-1].split("\n")
    f.close()

    checksum = solve(puzzle_input)

    print("The diagnostic checksum is " + str(checksum) + ".")

class AOC_Tests(unittest.TestCase):
    def test_ex1(self):
        self.assertEqual(solve(["Begin in state A.",
                                "Perform a diagnostic checksum after 6 steps.",
                                "",
                                "In state A:",
                                "  If the current value is 0:",
                                "    - Write the value 1.",
                                "    - Move one slot to the right.",
                                "    - Continue with state B.",
                                "  If the current value is 1:",
                                "    - Write the value 0.",
                                "    - Move one slot to the left.",
                                "    - Continue with state B.",
                                "",
                                "In state B:",
                                "  If the current value is 0:",
                                "    - Write the value 1.",
                                "    - Move one slot to the left.",
                                "    - Continue with state A.",
                                "  If the current value is 1:",
                                "    - Write the value 1.",
                                "    - Move one slot to the right.",
                                "    - Continue with state A."]), 3)

if __name__ == "__main__":
    if unittest.main(verbosity=2, exit=False, testRunner=util.tests.Runner).result.wasSuccessful():
        main()
        exit(0)
    else:
        exit(1)
