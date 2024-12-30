#!/usr/bin/env python3

#Advent of Code
#2018 Day 9, Part 2
#Solution by James C. (https://github.com/JamesMCo)

import os, sys
sys.path.append(os.path.abspath("../.."))
import unittest, util.read
from util.tests import run

from collections import deque

def solve(puzzle_input):
    marbles = deque([0])
    players = int(puzzle_input.split()[0])
    end     = int(puzzle_input.split()[6]) * 100
    scores  = [0 for p in range(players)]

    current_player = 0 #Index into scores list

    for m in range(1, end+1):
        if m % 23 == 0:
            scores[current_player] += m

            marbles.rotate(7)
            scores[current_player] += marbles.pop()

            marbles.rotate(-1)
        else:
            marbles.rotate(-1)
            marbles.append(m)

        current_player = (current_player + 1) % players

    return max(scores)

def main():
    puzzle_input = util.read.as_string()

    score = solve(puzzle_input)

    print("The winning elf's score is " + str(score) + ".")

class AOC_Tests(unittest.TestCase):
    @unittest.skip("No test cases")
    def test_ex1(self):
        pass

if __name__ == "__main__":
    run(main)
