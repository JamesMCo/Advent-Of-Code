#!/usr/bin/env python3

#Advent of Code
#2022 Day 2, Part 1
#Solution by James C. (https://github.com/JamesMCo)

import os, sys
sys.path.append(os.path.abspath("../.."))
import unittest, util.read
from util.tests import run

def solve(puzzle_input):
    class Shape:
        def __init__(self, letter):
            match letter:
                case "A" | "X":
                    self.shape = "rock"
                    self.score = 1
                case "B" | "Y":
                    self.shape = "paper"
                    self.score = 2
                case "C" | "Z":
                    self.shape = "scissors"
                    self.score = 3

        def beats(self, opponent):
            match self.shape:
                case "rock":     return opponent.shape == "scissors"
                case "paper":    return opponent.shape == "rock"
                case "scissors": return opponent.shape == "paper"

        def __eq__(self, other):
            return self.shape == other.shape

    def round_outcome(opponent, player):
        opponent = Shape(opponent)
        player   = Shape(player)

        if opponent.beats(player):
            # The opponent's move wins
            return 0
        elif opponent == player:
            # It's a tie
            return 3
        else:
            # The player's move wins
            return 6

    return sum(Shape(player).score + round_outcome(opponent, player) for opponent, player in [turn.split() for turn in puzzle_input])

def main():
    puzzle_input = util.read.as_lines()

    score = solve(puzzle_input)

    print("The total score is " + str(score) + ".")

class AOC_Tests(unittest.TestCase):
    def test_ex1(self):
        return self.assertEqual(solve(["A Y",
                                       "B X",
                                       "C Z"]), 15)

run(main)
