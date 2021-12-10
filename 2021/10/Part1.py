#!/usr/bin/env python3

#Advent of Code
#2021 Day 10, Part 1
#Solution by James C. (https://github.com/JamesMCo)

import os, sys
sys.path.append(os.path.abspath("../.."))
import unittest, util.read
from util.tests import run

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
                    raise ValueError(line[i + 1])
            else:
                i += 1
        return True

    def score(line):
        values = {")": 3, "]": 57, "}": 1197, ">": 25137}

        try:
            validate(line)
            return 0
        except ValueError as e:
            return values[e.args[0]]

    return sum(score(line) for line in puzzle_input)

def main():
    puzzle_input = util.read.as_lines()

    score = solve(puzzle_input)

    print("The total syntax error score is " + str(score) + ".")

class AOC_Tests(unittest.TestCase):
    def test_ex1(self):
        return self.assertEqual(solve(["[({(<(())[]>[[{[]{<()<>>",
                                       "[(()[<>])]({[<{<<[]>>(",
                                       "{([(<{}[<>[]}>{[]{[(<()>",
                                       "(((({<>}<{<{<>}{[]{[]{}",
                                       "[[<[([]))<([[{}[[()]]]",
                                       "[{[{({}]{}}([{[{{{}}([]",
                                       "{<[[]]>}<{[{[{[]{()[[[]",
                                       "[<(<(<(<{}))><([]([]()",
                                       "<{([([[(<>()){}]>(<<{{",
                                       "<{([{{}}[<[[[<>{}]]]>[]]"]), 26397)

run(main)
