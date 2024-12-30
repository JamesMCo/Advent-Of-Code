#!/usr/bin/env python3

#Advent of Code
#2021 Day 4, Part 2
#Solution by James C. (https://github.com/JamesMCo)

import os, sys
sys.path.append(os.path.abspath("../.."))
import unittest, util.read
from util.tests import run

def solve(puzzle_input):
    class Board:
        def __init__(self, board):
            self.board = board
            self.stamps = [[False for i in range(5)] for j in range(5)]
            self.has_won = False

        def stamp(self, n):
            if self.has_won:
                return False

            for y, row in enumerate(self.board):
                for x, col in enumerate(row):
                    if col == n:
                        self.stamps[y][x] = True
                        return self.check_win(x, y)
            return False

        def check_win(self, col, row):
            if all(self.stamps[row]) or all([r[col] for r in self.stamps]):
                self.has_won = True
                return self.score()
            return False

        def score(self):
            total = 0
            for y, row in enumerate(self.board):
                for x, col in enumerate(row):
                    if not self.stamps[y][x]:
                        total += col
            return total

    draw_pile = [int(x) for x in puzzle_input[0].split(",")]
    boards = []
    i = 2
    while i < len(puzzle_input):
        board = []
        for j in range(5):
            board.append([int(puzzle_input[i+j][k:k+2]) for k in range(0, 13, 3)])
        boards.append(Board(board))
        i += 6

    latest_winning_score = None
    latest_winning_n = None
    for n in draw_pile:
        for board in boards:
            if (value := board.stamp(n)):
                latest_winning_score = value
                latest_winning_n = n
    return latest_winning_score * latest_winning_n

def main():
    puzzle_input = util.read.as_lines()

    score = solve(puzzle_input)

    print("The score of the board that wins last is " + str(score) + ".")

class AOC_Tests(unittest.TestCase):
    def test_ex1(self):
        return self.assertEqual(solve(["7,4,9,5,11,17,23,2,0,14,21,24,10,16,13,6,15,25,12,22,18,20,8,19,3,26,1",
                                       "",
                                       "22 13 17 11  0",
                                       " 8  2 23  4 24",
                                       "21  9 14 16  7",
                                       " 6 10  3 18  5",
                                       " 1 12 20 15 19",
                                       "",
                                       " 3 15  0  2 22",
                                       " 9 18 13 17  5",
                                       "19  8  7 25 23",
                                       "20 11 10 24  4",
                                       "14 21 16 12  6",
                                       "",
                                       "14 21 17 24  4",
                                       "10 16 15  9 19",
                                       "18  8 23 26 20",
                                       "22 11 13  6  5",
                                       " 2  0 12  3  7"]), 1924)

if __name__ == "__main__":
    run(main)
