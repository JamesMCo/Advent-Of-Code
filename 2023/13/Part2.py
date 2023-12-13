#!/usr/bin/env python3

#Advent of Code
#2023 Day 13, Part 2
#Solution by James C. (https://github.com/JamesMCo)

import os, sys
sys.path.append(os.path.abspath("../.."))
import unittest, util.read
from util.tests import run

import typing as t

def solve(puzzle_input: list[str]) -> int:
    def find_reflection(pattern: list[str], original_reflection: t.Optional[int] = None) -> int:
        def is_reflection(n: int, pattern_candidate: list[str]) -> bool:
            return all(a == b for line in pattern_candidate for a, b in zip(line[:n][::-1], line[n:]))

        for x in range(1, len(pattern[0])):
            if is_reflection(x, pattern) and x != original_reflection:
                return x
        transposed_pattern = ["".join(row[col] for row in pattern) for col in range(len(pattern[0]))]
        for y in range(1, len(pattern)):
            if is_reflection(y, transposed_pattern) and y * 100 != original_reflection:
                return 100 * y
        return 0

    def get_smudges(pattern: list[str]) -> t.Iterable[list[str]]:
        for y in range(len(pattern)):
            for x in range(len(pattern[0])):
                output = pattern[:y]
                output.append(pattern[y][:x] + ("." if pattern[y][x] == "#" else "#") + pattern[y][x+1:])
                output.extend(pattern[y+1:])
                yield output

    def find_new_reflection(pattern: list[str]) -> int:
        original_reflection = find_reflection(pattern)

        for new_pattern in get_smudges(pattern):
            if new_reflection := find_reflection(new_pattern, original_reflection):
                return new_reflection

    def get_patterns() -> t.Iterable[list[str]]:
        output = []
        for line in puzzle_input:
            if line:
                output.append(line)
            else:
                yield output
                output = []
        yield output

    return sum(map(find_new_reflection, get_patterns()))

def main() -> tuple[str, int]:
    puzzle_input = util.read.as_lines()

    return "The result of summarising the notes finding the new reflection lines is {}.", solve(puzzle_input)

class AOC_Tests(unittest.TestCase):
    def test_ex1(self):
        return self.assertEqual(solve(["#.##..##.",
                                       "..#.##.#.",
                                       "##......#",
                                       "##......#",
                                       "..#.##.#.",
                                       "..##..##.",
                                       "#.#.##.#.",
                                       "",
                                       "#...##..#",
                                       "#....#..#",
                                       "..##..###",
                                       "#####.##.",
                                       "#####.##.",
                                       "..##..###",
                                       "#....#..#"]), 400)

run(main)
