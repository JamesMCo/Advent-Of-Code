#!/usr/bin/env python3

#Advent of Code
#2022 Day 2, Part 2
#Solution by James C. (https://github.com/JamesMCo)

import os, sys
sys.path.append(os.path.abspath("../.."))
import unittest, util.read
from util.tests import run

def solve(puzzle_input):
    class Shape:
        def __init__(self, letter):
            match letter:
                case "A" | "rock":
                    self.shape    = "rock"
                    self.score    = 1
                    self.wins_to  = "scissors"
                    self.loses_to = "paper"
                case "B" | "paper":
                    self.shape    = "paper"
                    self.score    = 2
                    self.wins_to  = "rock"
                    self.loses_to = "scissors"
                case "C" | "scissors":
                    self.shape    = "scissors"
                    self.score    = 3
                    self.wins_to  = "paper"
                    self.loses_to = "rock"

        def beats(self, opponent):
            return self.wins_to == opponent.shape

        def __eq__(self, other):
            return self.shape == other.shape

    def round_outcome(opponent, player):
        if opponent.beats(player):
            # The opponent's move wins
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
        opponent = Shape(opponent)
        match desired_outcome:
            case "X":
                # Need to lose
                # Play the move that the opponent beats
                player = Shape(opponent.wins_to)
            case "Y":
                # Need to tie
                # Play the same move as the opponent
                player = opponent
            case "Z":
                # Need to win
                # Play the move that beats the opponent, i.e. the move that the opponent is beaten by
                player = Shape(opponent.loses_to)

        total += player.score + round_outcome(opponent, player)

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
