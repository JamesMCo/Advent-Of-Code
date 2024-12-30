#!/usr/bin/env python3

#Advent of Code
#2021 Day 21, Part 2
#Solution by James C. (https://github.com/JamesMCo)

import os, sys
sys.path.append(os.path.abspath("../.."))
import unittest, util.read
from util.tests import run

from collections import Counter, defaultdict
from functools import cache

def solve(puzzle_input):
    possible_moves = [sum([a, b, c]) for a in range(1, 4) for b in range(1, 4) for c in range(1, 4)]
    move_quants = Counter(possible_moves)
    move_set = set(possible_moves)

    @cache
    def play(active_num, active_pos, active_score, inactive_num, inactive_pos, inactive_score, moves=0, start=True):
        if not start:
            if active_pos + moves <= 10:
                new_active_pos   = active_pos + moves
            else:
                new_active_pos   = active_pos + moves - 10
            new_active_score = active_score + new_active_pos

            if new_active_score >= 21:
                return {active_num: 1, inactive_num: 0}
        else:
            new_active_pos   = active_pos
            new_active_score = active_score

        results = defaultdict(int)
        for move in move_set:
            r = play(inactive_num, inactive_pos, inactive_score, active_num, new_active_pos, new_active_score, move, False)
            results[active_num] += r[active_num] * move_quants[move]
            results[inactive_num] += r[inactive_num] * move_quants[move]
        return results

    def make_player(description):
        return (int(description.split()[1]), int(description.split()[-1]), 0)

    player1 = make_player(puzzle_input[0])
    player2 = make_player(puzzle_input[1])
    return max([value for key, value in play(*player2, *player1).items()])

def main():
    puzzle_input = util.read.as_lines()

    wins = solve(puzzle_input)

    print("The number of universes that the most winning player wins in is " + str(wins) + ".")

class AOC_Tests(unittest.TestCase):
    def test_ex1(self):
        return self.assertEqual(solve(["Player 1 starting position: 4",
                                       "Player 2 starting position: 8"]), 444356092776315)

if __name__ == "__main__":
    run(main)
