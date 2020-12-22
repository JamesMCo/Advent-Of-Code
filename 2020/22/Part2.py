#!/usr/bin/env python3

#Advent of Code
#2020 Day 22, Part 2
#Solution by James C. (https://github.com/JamesMCo)

import os, sys
sys.path.append(os.path.abspath("../.."))
import unittest, util.read
from util.tests import run

from collections import deque

def solve(puzzle_input):
    def consume_section():
        output = []
        while puzzle_input:
            line = puzzle_input.pop(0)
            if line == "":
                break
            output.append(line)
        return output

    class Combat:
        def __init__(self, p1, p2):
            self.p1 = deque([int(card) for card in p1])
            self.p2 = deque([int(card) for card in p2])
            self.seen   = set()
            self.winner = 0

        def play(self):
            while True:
                if self.winner != 0:
                    return

                self.turn()

                if len(self.p1) == 0: self.winner = 2
                elif len(self.p2) == 0: self.winner = 1

        def turn(self):
            if (str(self.p1), str(self.p2)) in self.seen:
                self.winner = 1
                return
            self.seen.add((str(self.p1), str(self.p2)))

            p1_card = self.p1.popleft()
            p2_card = self.p2.popleft()

            if len(self.p1) >= p1_card and len(self.p2) >= p2_card:
                sub_game = Combat(list(self.p1)[:p1_card], list(self.p2)[:p2_card])
                sub_game.play()
                if sub_game.winner == 1:
                    self.p1.append(p1_card)
                    self.p1.append(p2_card)
                else:
                    self.p2.append(p2_card)
                    self.p2.append(p1_card)
            else:
                if p1_card > p2_card:
                    self.p1.append(p1_card)
                    self.p1.append(p2_card)
                else:
                    self.p2.append(p2_card)
                    self.p2.append(p1_card)

        def final_score(self):
            if len(self.p1) == 0:
                return sum([(multiplier+1) * card for multiplier, card in enumerate(reversed(self.p2))])
            else:
                return sum([(multiplier+1) * card for multiplier, card in enumerate(reversed(self.p1))])

    game = Combat(consume_section()[1:], consume_section()[1:])
    game.play()
    return game.final_score()

def main():
    puzzle_input = util.read.as_lines()

    score = solve(puzzle_input)

    print("The winning player's score is " + str(score) + ".")

class AOC_Tests(unittest.TestCase):
    def test_ex1(self):
        return self.assertEqual(solve(["Player 1:", "9", "2", "6", "3", "1", "",
                                       "Player 2:", "5", "8", "4", "7", "10"]), 291)

run(main)
