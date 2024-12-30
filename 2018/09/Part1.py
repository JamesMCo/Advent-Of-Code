#!/usr/bin/env python3

#Advent of Code
#2018 Day 9, Part 1
#Solution by James C. (https://github.com/JamesMCo)

import os, sys
sys.path.append(os.path.abspath("../.."))
import unittest, util.read
from util.tests import run

from collections import deque

def solve(puzzle_input):
    marbles = deque([0])
    players = int(puzzle_input.split()[0])
    end     = int(puzzle_input.split()[6])
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
    def test_ex1(self):
        self.assertEqual(solve("9 players; last marble is worth 25 points"), 32)

    def test_ex2(self):
        self.assertEqual(solve("10 players; last marble is worth 1618 points"), 8317)

    def test_ex3(self):
        self.assertEqual(solve("13 players; last marble is worth 7999 points"), 146373)

    def test_ex4(self):
        self.assertEqual(solve("17 players; last marble is worth 1104 points"), 2764)

    def test_ex5(self):
        self.assertEqual(solve("21 players; last marble is worth 6111 points"), 54718)

    def test_ex6(self):
        self.assertEqual(solve("30 players; last marble is worth 5807 points"), 37305)

if __name__ == "__main__":
    run(main)
