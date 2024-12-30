#!/usr/bin/env python3

#Advent of Code
#2023 Day 12, Part 1
#Solution by James C. (https://github.com/JamesMCo)

import os, sys
sys.path.append(os.path.abspath("../.."))
import unittest, util.read
from util.tests import run

from functools import cache
from itertools import starmap

def solve(puzzle_input: list[str]) -> int:
    @cache
    def count_arrangements(springs: str, groups: tuple[int, ...]) -> int:
        # Based on the implementation described in this reddit comment by /u/damaltor1
        # https://www.reddit.com/r/adventofcode/comments/18ghux0/comment/kd0npmi/

        if groups:
            if not springs:
                # No more springs, but still groups
                return 0
        elif springs:
            if "#" in springs:
                # At least one broken spring, but no groups for it to be a part of
                return 0
        else:
            # No springs, and no groups
            # Only one way to arrange nothing
            return 1

        match springs[0]:
            case ".":
                # Step once into the list
                return count_arrangements(springs[1:], groups)
            case "#":
                # n = number of springs in the first group
                # If the list starts with n broken springs, and either the group reaches the end of the list or is followed by a non-broken spring,
                # then recurse without the broken springs, the separating non-broken spring (i.e. skip n+1 springs), and the group descriptor
                # ? can count as # for the group check, and ? can count as . for the separating check
                if len(springs) < groups[0]:
                    # There are not enough springs to make the group valid
                    return 0
                elif all(c in "#?" for c in springs[:groups[0]]):
                    # There are enough springs to make the group valid
                    if len(springs) == groups[0]:
                        # The entire list of springs is this group
                        if len(groups) == 1:
                            # And the only group remaining is this group
                            return 1
                        else:
                            # There are more groups that need to be considered, and therefore
                            # this is invalid
                            return 0
                    else:
                        # There are more springs than just this group
                        if springs[groups[0]] in ".?":
                            # The spring after the group can act as a separator
                            return count_arrangements(springs[groups[0] + 1:], groups[1:])
                        else:
                            # The spring after the group is also broken, and cannot act as a separator
                            # This is invalid
                            return 0
                else:
                    # There are not only broken springs in the space that should be taken by the group
                    # This is invalid
                    return 0
            case "?":
                # Replace ? with both . and # and sum the total arrangements from both
                a = count_arrangements("." + springs[1:], groups)
                b = count_arrangements("#" + springs[1:], groups)
                return a + b

    def parse_line(line: str) -> tuple[str, tuple[int, ...]]:
        springs, groups = line.split()
        return springs, tuple(map(int, groups.split(",")))

    return sum(starmap(count_arrangements, map(parse_line, puzzle_input)))

def main() -> tuple[str, int]:
    puzzle_input = util.read.as_lines()

    return "The sum of the arrangements for all lines is {}.", solve(puzzle_input)

class AOC_Tests(unittest.TestCase):
    def test_ex1(self):
        return self.assertEqual(solve(["???.### 1,1,3",
                                       ".??..??...?##. 1,1,3",
                                       "?#?#?#?#?#?#?#? 1,3,1,6",
                                       "????.#...#... 4,1,1",
                                       "????.######..#####. 1,6,5",
                                       "?###???????? 3,2,1"]), 21)

if __name__ == "__main__":
    run(main)
