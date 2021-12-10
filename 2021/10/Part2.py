#!/usr/bin/env python3

#Advent of Code
#2021 Day 10, Part 2
#Solution by James C. (https://github.com/JamesMCo)

import os, sys
sys.path.append(os.path.abspath("../.."))
import unittest, util.read
from util.tests import run

from functools import reduce

def solve(puzzle_input):
    is_opener = lambda c: c in "([{<"
    is_closer = lambda c: c in ")]}>"
    def open_matches_close(o, c):
        match (o, c):
            case ("(", ")"): return True
            case ("[", "]"): return True
            case ("{", "}"): return True
            case ("<", ">"): return True
            case (_, _):     return False

    def validate(line):
        i = 0
        while i + 1 < len(line):
            if is_opener(line[i]) and is_closer(line[i + 1]):
                if open_matches_close(line[i], line[i + 1]):
                    return validate(line[:i] + line[i + 2:])
                else:
                    return False
            else:
                i += 1
        return True

    def remove_closed_chunks(line):
        i = 0
        while i + 1 < len(line):
            if is_opener(line[i]) and is_closer(line[i + 1]):
                # Known to be valid, so don't need to check if open/close match
                return remove_closed_chunks(line[:i] + line[i + 2:])
            else:
                i += 1
        return line

    def score(line):
        values = {"(": 1, "[": 2, "{": 3, "<": 4}
        return reduce(lambda total, c: (total * 5) + values[c], remove_closed_chunks(line)[::-1], 0)

    scores = sorted(score(line) for line in puzzle_input if validate(line))
    return scores[int(len(scores)/2)]

def main():
    puzzle_input = util.read.as_lines()

    score = solve(puzzle_input)

    print("The middle score is " + str(score) + ".")

class AOC_Tests(unittest.TestCase):
    def test_ex1(self):
        return self.assertEqual(solve(["[({(<(())[]>[[{[]{<()<>>",
                                       "[(()[<>])]({[<{<<[]>>(",
                                       "(((({<>}<{<{<>}{[]{[]{}",
                                       "{<[[]]>}<{[{[{[]{()[[[]",
                                       "<{([{{}}[<[[[<>{}]]]>[]]"]), 288957)

run(main)
