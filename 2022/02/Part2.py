#!/usr/bin/env python3

#Advent of Code
#2022 Day 2, Part 2
#Solution by James C. (https://github.com/JamesMCo)

import os, sys
sys.path.append(os.path.abspath("../.."))
import unittest, util.read
from util.tests import run

def solve(puzzle_input):
    moves = {
        "A": "rock",
        "B": "paper",
        "C": "scissors"
    }
    beats = {
        "rock":     "scissors",
        "paper":    "rock",
        "scissors": "paper"
    }
    beaten_by = {
        "rock":     "paper",
        "paper":    "scissors",
        "scissors": "rock"
    }
    shape_score = {
        "rock":     1,
        "paper":    2,
        "scissors": 3
    }

    def round_outcome(opponent, player):
        if beats[opponent] == player:
            # The move that the opponent's move beats is the move that the player made
            return 0
        elif opponent == player:
            # It's a tie
            return 3
        else:
            # The player's move wins
            return 6

    total = 0
    for turn in puzzle_input:
        opponent, desired_outcome = turn.split()
        opponent = moves[opponent]
        if desired_outcome == "X":
            # Need to lose
            # Play the move that the opponent beats
            player = beats[opponent]
        elif desired_outcome == "Y":
            # Need to tie
            # Play the same move as the opponent
            player = opponent
        else:
            # Need to win
            # Play the move that beats the opponent, i.e. the move that the opponent is beaten by
            player = beaten_by[opponent]

        total += shape_score[player] + round_outcome(opponent, player)

    return total

def main():
    puzzle_input = util.read.as_lines()

    score = solve(puzzle_input)

    print("The total score is " + str(score) + ".")

class AOC_Tests(unittest.TestCase):
    def test_ex1(self):
        return self.assertEqual(solve(["A Y",
                                       "B X",
                                       "C Z"]), 12)

run(main)
