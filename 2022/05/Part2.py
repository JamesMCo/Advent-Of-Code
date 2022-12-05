#!/usr/bin/env python3

#Advent of Code
#2022 Day 5, Part 2
#Solution by James C. (https://github.com/JamesMCo)

import os, sys
sys.path.append(os.path.abspath("../.."))
import unittest, util.read
from util.tests import run

import re

def solve(puzzle_input):
    def parse_stacks(lines):
        stacks = []
        for i, line in enumerate(lines):
            if line[1] == "1":
                return [stack[::-1] for stack in stacks], i

            for stack_num, pos_in_line in enumerate(range(1, len(line), 4)):
                if i == 0:
                    if line[pos_in_line] != " ":
                        stacks.append([line[pos_in_line]])
                    else:
                        stacks.append([])
                else:
                    if line[pos_in_line] != " ":
                        stacks[stack_num].append(line[pos_in_line])

    def manipulate_stacks(stacks, instructions):
        for instruction in instructions:
            quant, from_stack, to_stack = [int(x) for x in re.match("move (\d+) from (\d+) to (\d+)", instruction).groups()]

            # Stacks are one-indexed in puzzle input, but zero-indexed in list
            from_stack -= 1
            to_stack -= 1

            lifted_crates = stacks[from_stack][-quant:]
            for crate in range(quant):
                stacks[from_stack].pop()
            stacks[to_stack].extend(lifted_crates)

        return stacks

    stacks, line_of_indices = parse_stacks(puzzle_input)
    stacks = manipulate_stacks(stacks, puzzle_input[line_of_indices+2:])

    return "".join([stack[-1] for stack in stacks])

def main():
    puzzle_input = util.read.as_lines_only_rstrip()

    crates = solve(puzzle_input)

    print("The crates is " + str(crates) + ".")

class AOC_Tests(unittest.TestCase):
    def test_ex1(self):
        return self.assertEqual(solve(["    [D]    ",
                                       "[N] [C]    ",
                                       "[Z] [M] [P]",
                                       " 1   2   3 ",
                                       "",
                                       "move 1 from 2 to 1",
                                       "move 3 from 1 to 3",
                                       "move 2 from 2 to 1",
                                       "move 1 from 1 to 2"]), "MCD")

run(main)
