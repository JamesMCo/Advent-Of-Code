#!/usr/bin/env python3

#Advent of Code
#2025 Day 12, Part 1
#Solution by James C. (https://github.com/JamesMCo)

import os, sys
sys.path.append(os.path.abspath("../.."))
import unittest, util.read
from util.tests import run

from itertools import dropwhile, takewhile
from pathos.pools import ProcessPool as Pool
from typing import Iterable

def solve(puzzle_input: list[str]) -> int:
    def parse_present(present: list[str]) -> set[tuple[int, int]]:
        output: set[tuple[int, int]] = set()
        for y, row in enumerate(present):
            for x, col in enumerate(row):
                if col == "#":
                    output.add((x, y))
        return output

    def rotate(present: list[str]) -> list[str]:
        return ["".join(cols) for cols in zip(*present)]

    def flip(present: list[str]) -> list[str]:
        return [line[::-1] for line in present]

    def get_all_rotations_and_flips(present: list[str]) -> list[set[tuple[int, int]]]:
        rotations_and_flips: Iterable[set[tuple[int, int]]] = map(parse_present, [
            present,
            rotate(present),
            rotate(rotate(present)),
            rotate(rotate(rotate(present))),
            flip(present),
            rotate(flip(present)),
            rotate(rotate(flip(present))),
            rotate(rotate(rotate(flip(present)))),
        ])

        unique: list[set[tuple[int, int]]] = []
        for candidate in rotations_and_flips:
            if not any(candidate == existing for existing in unique):
                unique.append(candidate)
        return unique

    presents: list[list[set[tuple[int, int]]]] = []
    present_cellcount: list[int] = []

    present_descriptions: Iterable[str] = reversed(list(dropwhile(lambda l: l != "", reversed(puzzle_input))))
    current_present: list[str] = []
    for i, l in enumerate(present_descriptions):
        if ":" in l:
            continue
        elif "." in l or "#" in l:
            current_present.append(l)
        else:
            presents.append(get_all_rotations_and_flips(current_present))
            present_cellcount.append(len(presents[-1][0]))
            current_present = []

    def is_possible(region_description: str) -> bool:
        width_str, height_str = region_description.split(":")[0].split("x")
        width: int = int(width_str)
        height: int = int(height_str)
        required_presents: list[int] = [int(n) for n in region_description.split()[1:]]

        # Sanity check: if the number of cells occupied by the number of presents requested
        #               is greater than the total area, then it's not possible
        if sum(count * size for count, size in zip(required_presents, present_cellcount)) > width * height:
            return False

        present_pool: list[list[set[tuple[int, int]]]] = []
        for count, present in zip(required_presents, presents):
            for c in range(count):
                present_pool.append(present)

        seen: set[str] = set()

        def try_to_fit(currently_placed: set[tuple[int, int]], remaining_presents: list[list[set[tuple[int, int]]]]) -> bool:
            if not remaining_presents:
                # All presents have been placed!
                return True
            elif str(sorted(currently_placed)) in seen:
                # We've seen this exact pattern of placed cells before, so we can't fit all the presents
                # (otherwise we'd have returned True all the way up the callstack and wouldn't be here).
                return False
            else:
                seen.add(str(sorted(currently_placed)))
                for x in range(width):
                    for y in range(height):
                        # Candidates are rotations/flips of the first remaining present in the list
                        for candidate in remaining_presents[0]:
                            if any(x + dx >= width or y + dy >= height for dx, dy in candidate):
                                # Can't place presents outside the region.
                                continue
                            if any((x + dx, y + dy) in currently_placed for dx, dy in candidate):
                                # Can't overlap presents.
                                continue

                            if try_to_fit(currently_placed.union([(x + dx, y + dy) for dx, dy in candidate]), remaining_presents[1:]):
                                # We were able to place all presents without overlapping!
                                return True
                # We couldn't place the remaining presents with this starting state.
                return False

        return try_to_fit(set(), present_pool[:])

    with Pool() as pool:
        return sum(pool.imap(is_possible, reversed(list(takewhile(lambda l: l != "", reversed(puzzle_input))))))

def main() -> tuple[str, int]:
    puzzle_input = util.read.as_lines()

    return "The number of regions that can fit all of the presents listed is {}.", solve(puzzle_input)

class AOC_Tests(unittest.TestCase):
    def test_ex1(self):
        return self.assertEqual(solve(["0:",
                                       "###",
                                       "##.",
                                       "##.",
                                       "",
                                       "1:",
                                       "###",
                                       "##.",
                                       ".##",
                                       "",
                                       "2:",
                                       ".##",
                                       "###",
                                       "##.",
                                       "",
                                       "3:",
                                       "##.",
                                       "###",
                                       "##.",
                                       "",
                                       "4:",
                                       "###",
                                       "#..",
                                       "###",
                                       "",
                                       "5:",
                                       "###",
                                       ".#.",
                                       "###",
                                       "",
                                       "4x4: 0 0 0 0 2 0",
                                       "12x5: 1 0 1 0 2 2",
                                       "12x5: 1 0 1 0 3 2"]), 2)

if __name__ == "__main__":
    run(main)
