#!/usr/bin/env python3

#Advent of Code
#2023 Day 5, Part 1
#Solution by James C. (https://github.com/JamesMCo)

import os, sys
sys.path.append(os.path.abspath("../.."))
import unittest, util.read
from util.tests import run

import re
import typing as t

def solve(puzzle_input: list[str]) -> int:
    seeds: list[int] = []
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

            maps[self.from_type] = self

        def __call__(self: t.Self, value: int) -> int:
            for dest, source, length in self.ranges:
                if source <= value < source + length:
                    return (value - source) + dest
            return value

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
            seeds = list(map(int, re.findall(r"\d+", section[0])))
        else:
            # RangeMap.__init__() saves a reference to itself in the maps dict
            RangeMap(section)

    def find_location_for_seed(seed: int):
        from_type = "seed"
        value = seed

        while True:
            current_map: RangeMap = maps[from_type]

            from_type, value = current_map.to_type, current_map(value)

            if from_type == "location":
                return value

    return min(map(find_location_for_seed, seeds))

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
                                       "56 93 4"]), 35)

run(main)
