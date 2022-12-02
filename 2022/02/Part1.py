#!/usr/bin/env python3

#Advent of Code
#2022 Day 2, Part 1
#Solution by James C. (https://github.com/JamesMCo)

import os, sys
sys.path.append(os.path.abspath("../.."))
import unittest, util.read
from util.tests import run

def solve(puzzle_input):
    moves = {
        "A": "rock",
        "B": "paper",
        "C": "scissors",
        "X": "rock",
        "Y": "paper",
        "Z": "scissors"
    }
    beats = {
        "rock":     "scissors",
        "paper":    "rock",
        "scissors": "paper"
    }
    shape_score = {
        "rock":     1,
        "paper":    2,
        "scissors": 3
    }

    def round_outcome(opponent, player):
        opponent = moves[opponent]
        player   = moves[player]

        if beats[opponent] == player:
            # The move that the opponent's move beats is the move that the player made
            return 0
        elif opponent == player:
            # It's a tie
            return 3
        else:
            # The player's move wins
            return 6

    return sum(shape_score[moves[player]] + round_outcome(opponent, player) for opponent, player in [turn.split() for turn in puzzle_input])

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
