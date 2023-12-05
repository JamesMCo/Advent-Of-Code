#!/usr/bin/env python3

#Advent of Code
#2023 Day 5, Part 2
#Solution by James C. (https://github.com/JamesMCo)

import os, sys
sys.path.append(os.path.abspath("../.."))
import unittest, util.read
from util.tests import run

from itertools import batched
import re
import typing as t

def solve(puzzle_input: list[str]) -> int:
    seed_ranges: list[tuple[int, int]] = []
    maps: dict[str, "RangeMap"] = {}

    class RangeMap:
        from_type: str
        to_type: str
        ranges: list[tuple[int, int, int]]

        name_pattern: re.Pattern = re.compile(r"(\w+)-to-(\w+) map:")
        ranges_pattern: re.Pattern = re.compile(r"(\d+) (\d+) (\d+)")

        def __init__(self: t.Self, section_definition: list[str]) -> None:
            self.from_type, self.to_type = self.name_pattern.match(section_definition[0]).groups()

            self.ranges = []
            for range_definition in section_definition[1:]:
                dest, source, length = self.ranges_pattern.match(range_definition).groups()
                self.ranges.append((int(dest), int(source), int(length)))
            self.ranges.sort(key=lambda r: r[1])

            maps[self.from_type] = self

        def __call__(self: t.Self, value: int) -> int:
            for dest, source, length in self.ranges:
                if source <= value < source + length:
                    return (value - source) + dest
            return value

        @staticmethod
        def overlapping_range(a_start: int, a_end: int, b_start: int, b_end: int) -> t.Optional[tuple[int, int]]:
            # Check whether there is any overlap before trying to find what range is overlapping
            # https://stackoverflow.com/a/3269471
            if not (a_start <= b_end and a_end >= b_start):
                return None

            # A starts before or at same point as B, A ends within or at same point as B
            if a_start <= b_start and a_end <= b_end:
                return b_start, a_end

            # A starts before or at same point as B, A ends after B (B is entirely enclosed by A)
            if a_start <= b_start and b_end < a_end:
                return b_start, b_end

            # B starts before or at same point as A, B ends within or at same point as A
            if b_start <= a_start and b_end <= a_end:
                return a_start, b_end

            # B starts before or at same point as A, B ends after A (A is entirely enclosed by B)
            if b_start <= a_start and a_end < b_end:
                return a_start, a_end

        def transformed_range(self: t.Self, query_start: int, query_end: int) -> list[tuple[int, int]]:
            overlapping_ranges: list[tuple[int, int]] = []
            for r in self.ranges:
                if overlapping_range := self.overlapping_range(r[1], r[1] + r[2], query_start, query_end):
                    overlapping_ranges.append(overlapping_range)

            # Fill in gaps where ranges are not transformed but just returned as-is
            all_ranges: list[tuple[int, int]] = []
            if not overlapping_ranges:
                all_ranges.append((query_start, query_end))
            else:
                if overlapping_ranges[0][0] != query_start:
                    all_ranges.append((query_start, overlapping_ranges[0][0]))

                if len(overlapping_ranges) == 1:
                    all_ranges.append(overlapping_ranges[0])
                else:
                    for before, after in zip(overlapping_ranges[:-1], overlapping_ranges[1:]):
                        all_ranges.append(before)

                        if before[-1] != after[0]:
                            all_ranges.append((before[1], after[0]))

                        if after == overlapping_ranges[-1]:
                            all_ranges.append(after)

                if overlapping_ranges[-1][1] != query_end:
                    all_ranges.append((overlapping_ranges[-1][1], query_end))

            return [(self.__call__(r[0]), self.__call__(r[1] - 1)) for r in all_ranges]

    def get_sections() -> t.Iterable[list[str]]:
        output: list[str] = []

        for line in puzzle_input:
            if line:
                output.append(line)
            else:
                yield output
                output = []

        if output:
            yield output

    for i, section in enumerate(get_sections()):
        if i == 0:
            seed_ranges = list(batched(map(int, re.findall(r"\d+", section[0])), 2))
        else:
            # RangeMap.__init__() saves a reference to itself in the maps dict
            RangeMap(section)

    def find_location_for_seed_range(seed_range: tuple[int, int]) -> int:
        from_type = "seed"
        current_ranges: list[tuple[int, int]] = [(seed_range[0], seed_range[0] + seed_range[1])]

        while True:
            current_map: RangeMap = maps[from_type]

            from_type = current_map.to_type
            new_ranges = []
            for r in current_ranges:
                new_ranges.extend(current_map.transformed_range(*r))
            current_ranges = new_ranges

            if from_type == "location":
                return min(r[0] for r in current_ranges)

    return min(map(find_location_for_seed_range, seed_ranges))

def main() -> tuple[str, int]:
    puzzle_input = util.read.as_lines()

    return "The lowest location number that corresponds to any of the initial seeds is {}.", solve(puzzle_input)

class AOC_Tests(unittest.TestCase):
    def test_ex1(self):
        return self.assertEqual(solve(["seeds: 79 14 55 13",
                                       "",
                                       "seed-to-soil map:",
                                       "50 98 2",
                                       "52 50 48",
                                       "",
                                       "soil-to-fertilizer map:",
                                       "0 15 37",
                                       "37 52 2",
                                       "39 0 15",
                                       "",
                                       "fertilizer-to-water map:",
                                       "49 53 8",
                                       "0 11 42",
                                       "42 0 7",
                                       "57 7 4",
                                       "",
                                       "water-to-light map:",
                                       "88 18 7",
                                       "18 25 70",
                                       "",
                                       "light-to-temperature map:",
                                       "45 77 23",
                                       "81 45 19",
                                       "68 64 13",
                                       "",
                                       "temperature-to-humidity map:",
                                       "0 69 1",
                                       "1 0 69",
                                       "",
                                       "humidity-to-location map:",
                                       "60 56 37",
                                       "56 93 4"]), 46)

run(main)
