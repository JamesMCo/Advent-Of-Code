#!/usr/bin/env python3

#Advent of Code
#Day 19, Part 1
#Solution by James C. (https://github.com/JamesMCo)

import os, sys
sys.path.append(os.path.abspath("../.."))
import unittest
from util.tests import run

import string

def solve(puzzle_input):
    direction = "d"
    seen   = ""
    cur_x  = 0
    cur_y  = 0
    prev_x = -1
    prev_y = -1
    max_x  = len(puzzle_input[0])
    max_y  = len(puzzle_input)

    spaces = "|-+" + string.ascii_uppercase

    while puzzle_input[0][cur_x] != "|":
        cur_x += 1

    while (cur_x, cur_y) != (prev_x, prev_y):
        prev_x, prev_y = cur_x, cur_y

        if puzzle_input[cur_y][cur_x] == "+":
            if direction in "ud":
                if cur_x != max_x and puzzle_input[cur_y][cur_x+1] in spaces:
                    cur_x += 1
                    direction = "r"
                elif cur_x != 0 and puzzle_input[cur_y][cur_x-1] in spaces:
                    cur_x -= 1
                    direction = "l"
            else:
                if cur_y != max_y and puzzle_input[cur_y+1][cur_x] in spaces:
                    cur_y += 1
                    direction = "d"
                elif cur_y != 0 and puzzle_input[cur_y-1][cur_x] in spaces:
                    cur_y -= 1
                    direction = "u"
        elif direction == "d":
            if cur_y != max_y and puzzle_input[cur_y+1][cur_x] in spaces:
                cur_y += 1
        elif direction == "u":
            if cur_y != 0 and puzzle_input[cur_y-1][cur_x] in spaces:
                cur_y -= 1
        elif direction == "l":
            if cur_x != 0 and puzzle_input[cur_y][cur_x-1] in spaces:
                cur_x -= 1
        elif direction == "r":
            if cur_x != max_x and puzzle_input[cur_y][cur_x+1] in spaces:
                cur_x += 1

        if puzzle_input[cur_y][cur_x] in string.ascii_uppercase and (cur_x, cur_y) != (prev_x, prev_y):
            seen += puzzle_input[cur_y][cur_x]

    return seen

def main():
    f = open("puzzle_input.txt")
    puzzle_input = f.read()[:-1].split("\n")
    f.close()

    letters = solve(puzzle_input)

    print("The letters the packet sees on its path are " + str(letters) + ".")

class AOC_Tests(unittest.TestCase):
    def test_ex1(self):
        self.assertEqual(solve(["     |          ",
                                "     |  +--+    ",
                                "     A  |  C    ",
                                " F---|----E|--+ ",
                                "     |  |  |  D ",
                                "     +B-+  +--+ ",
                                "                "]), "ABCDEF")

run(main)
