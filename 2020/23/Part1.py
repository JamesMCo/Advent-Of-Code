#!/usr/bin/env python3

#Advent of Code
#2020 Day 23, Part 1
#Solution by James C. (https://github.com/JamesMCo)

import os, sys
sys.path.append(os.path.abspath("../.."))
import unittest, util.read
from util.tests import run

from collections import deque

def solve(puzzle_input, moves=100):
    class CupsGame:
        def __init__(self, initial_order):
            self.cups = deque([int(cup) for cup in initial_order])

        def play(self, moves):
            for move in range(moves):
                self.turn()

        def turn(self):
            current_cup = self.cups[0]

            self.cups.rotate(-1)
            removed_cups = [self.cups.popleft() for cup in range(3)]

            destination = self.find_next_destination(current_cup)

            self.cups.rotate(-1 - self.cups.index(destination))
            self.cups.extend(removed_cups)

            self.cups.rotate(-1 - self.cups.index(current_cup))

        def find_next_destination(self, current_cup):
            candidate = current_cup - 1
            while True:
                if candidate < min(self.cups):
                    candidate = max(self.cups)

                if candidate in self.cups:
                    return candidate

                candidate -= 1

        def order_from_one(self):
            cups = list(self.cups)
            return "".join([str(cup) for cup in cups[cups.index(1)+1:]]) + "".join([str(cup) for cup in cups[:cups.index(1)]])

    game = CupsGame(puzzle_input)
    game.play(moves)
    return game.order_from_one()

def main():
    puzzle_input = util.read.as_string()

    order = solve(puzzle_input)

    print("The order of the cups is " + str(order) + ".")

class AOC_Tests(unittest.TestCase):
    def test_ex1(self):
        return self.assertEqual(solve("389125467", 10), "92658374")

    def test_ex2(self):
        return self.assertEqual(solve("389125467"), "67384529")

if __name__ == "__main__":
    run(main)
