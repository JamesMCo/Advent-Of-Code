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
    def parse_input(puzzle_input):
        separator = puzzle_input.index("")
        stacks_description = puzzle_input[:separator]
        instructions = puzzle_input[separator+1:]

        # Find the number of stacks (number of stack labels just above the separator line)
        number_of_stacks = len(re.findall("\d+", puzzle_input[separator - 1]))
        # Create enough empty stacks in a list
        stacks = [[] for stack in range(number_of_stacks)]
        # Matches "[X]" or "   ", followed by an optional space, finding this "number_of_stacks" times on one line
        row_pattern = re.compile("(?:(?:\[(\w)\]| {3}) ?)" * number_of_stacks)

        # Reverse the stacks described in the puzzle input (i.e. work from bottom to top)
        for row in stacks_description[:-1][::-1]:
            for i, crate in enumerate(re.match(row_pattern, row).groups()):
                # If a crate exists, create equals that letter. Otherwise, it equals None.
                if crate:
                    stacks[i].append(crate)

        return stacks, instructions

    def manipulate_stacks(stacks, instructions):
        for instruction in instructions:
            quant, from_stack, to_stack = [int(x) for x in re.match("move (\d+) from (\d+) to (\d+)", instruction).groups()]

            # Stacks are one-indexed in puzzle input, but zero-indexed in list
            from_stack -= 1
            to_stack -= 1

            lifted_crates = stacks[from_stack][-quant:]
            del stacks[from_stack][-quant:]
            stacks[to_stack].extend(lifted_crates)

        return stacks

    # The top of the each stack is at the end of the list
    return "".join([stack[-1] for stack in manipulate_stacks(*parse_input(puzzle_input))])

def main():
    puzzle_input = util.read.as_lines_only_rstrip()

    crates = solve(puzzle_input)

    print("The crates on top of the stacks are " + str(crates) + ".")

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
