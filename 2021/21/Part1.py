#!/usr/bin/env python3

#Advent of Code
#2021 Day 21, Part 1
#Solution by James C. (https://github.com/JamesMCo)

import os, sys
sys.path.append(os.path.abspath("../.."))
import unittest, util.read
from util.tests import run

def solve(puzzle_input):
    class Player:
        def __init__(self, description):
            self.num = int(description.split()[1])
            self.pos = int(description.split()[-1])
            self.score = 0

        def turn(self, die):
            rolls = [next(die) for i in range(3)]
            moves = sum(rolls)
            while moves > 10:
                moves -= 10

            self.pos += moves
            if self.pos > 10:
                self.pos -= 10

            self.score += self.pos
            return self.score >= 1000

    class Die:
        def __init__(self):
            self.rolls = 0
            self.last_val = 0

        def __next__(self):
            self.rolls += 1
            self.last_val += 1
            if self.last_val > 100:
                self.last_val = 1
            return self.last_val

    players = [Player(l) for l in puzzle_input]
    die = Die()

    while True:
        for player in players:
            if player.turn(die):
                return sorted(players, key=lambda p: p.score)[0].score * die.rolls

def main():
    puzzle_input = util.read.as_lines()

    losingscore_dicerolls = solve(puzzle_input)

    print("The product of the losing player's score and the number of dice rolls is " + str(losingscore_dicerolls) + ".")

class AOC_Tests(unittest.TestCase):
    def test_ex1(self):
        return self.assertEqual(solve(["Player 1 starting position: 4",
                                       "Player 2 starting position: 8"]), 739785)

if __name__ == "__main__":
    run(main)
