#!/usr/bin/env python3

#Advent of Code
#2022 Day 15, Part 2
#Solution by James C. (https://github.com/JamesMCo)

import os, sys
sys.path.append(os.path.abspath("../.."))
import unittest, util.read
from util.tests import run

from functools import cache
from math import inf
import re
from util.two_d_world import manhattan_distance

def solve(puzzle_input, max_coord=4000000):
    puzzle_input = [[int(x) for x in re.match("Sensor at x=(-?\d+), y=(-?\d+): closest beacon is at x=(-?\d+), y=(-?\d+)", line).groups()] for line in puzzle_input]

    def combine_ranges(ranges):
        if not ranges:
            return []

        ranges.sort(key=lambda x: x[0])
        combined_ranges = [ranges[0]]
        for lower, upper in ranges[1:]:
            if combined_ranges[-1][0] <= lower <= combined_ranges[-1][1]:
                if combined_ranges[-1][1] < upper:
                    # This range extends the previous range (lower is within, upper is greater than)
                    combined_ranges[-1] = (combined_ranges[-1][0], upper)
                # Otherwise, the range is fully contained by the previous range, so we don't need to do anything
            elif combined_ranges[-1][0] + 1 == lower:
                # This range begins immediately after the previous range, so can extend anyway
                combined_ranges[-1] = (combined_ranges[-1][0], upper)
            else:
                # No intersection with previous range
                combined_ranges.append((lower, upper))

        return combined_ranges

    @cache
    def find_ranges(target_row):
        ranges = []
        for line in puzzle_input:
            sensor_x, sensor_y, beacon_x, beacon_y = line

            distance = manhattan_distance(sensor_x, sensor_y, beacon_x, beacon_y)
            half_width = distance - abs(target_row - sensor_y)
            if half_width >= 0:
                ranges.append((sensor_x - half_width, sensor_x + half_width))
        return combine_ranges(ranges)

    def clamp_ranges(ranges):
        valid_ranges = []
        for lower, upper in ranges:
            if 0 <= lower <= upper <= max_coord:
                # The range is fully within the valid range
                valid_ranges.append((lower, upper))
            elif upper < 0:
                # The range is fully below the valid range, and so shouldn't be included
                continue
            elif lower > max_coord:
                # The range is fully above the valid range, and so shouldn't be included.
                # No further ranges need to be considered, as they are sorted by the lower bound
                # and all further ranges will start above the valid range.
                return valid_ranges
            elif lower < 0 and 0 <= upper <= max_coord:
                # The range starts below the valid range and ends within it
                valid_ranges.append((0, upper))
            elif 0 <= lower <= max_coord and max_coord < upper:
                # The range starts within the valid range and ends above it
                valid_ranges.append((lower, max_coord))
                # No further ranges need to be considered, as they are sorted by the lower bound
                # and all further ranges will start either during this range (which is already
                # considered fully) or above the valid range.
                return valid_ranges

    def find_inverted_ranges(ranges):
        if len(ranges) == 0:
            return [(0, max_coord)]
        elif len(ranges) == 1:
            return clamp_ranges([(-inf, ranges[0][0]-1), (ranges[0][1]+1, inf)])
        else:
            inverted_ranges = [(-inf, ranges[0][0]-1)]
            for lower_range, upper_range in zip(ranges, ranges[1:]):
                inverted_ranges.append((lower_range[1]+1, upper_range[0]-1))
            inverted_ranges.append((ranges[-1][1]+1, inf))
            return clamp_ranges(inverted_ranges)

    @cache
    def find_inverted_row(target_row):
        return find_inverted_ranges(find_ranges(target_row))

    def in_ranges(x, ranges):
        return ranges and any(r[0] <= x <= r[1] for r in ranges)
    
    for y in range(max_coord+1):
        if not (current := find_inverted_row(y)):
            # No possible gaps
            continue

        above = find_ranges(y - 1)
        below = find_ranges(y + 1)
        for x in range(max_coord+1):
            if in_ranges(x, current) and in_ranges(x, above) and in_ranges(x, below):
                return (x * 4000000) + y

def main():
    puzzle_input = util.read.as_lines()

    empty = solve(puzzle_input)

    print("The tuning frequency of the distress beacon's position is " + str(empty) + ".")

class AOC_Tests(unittest.TestCase):
    def test_ex1(self):
        return self.assertEqual(solve(["Sensor at x=2, y=18: closest beacon is at x=-2, y=15",
                                       "Sensor at x=9, y=16: closest beacon is at x=10, y=16",
                                       "Sensor at x=13, y=2: closest beacon is at x=15, y=3",
                                       "Sensor at x=12, y=14: closest beacon is at x=10, y=16",
                                       "Sensor at x=10, y=20: closest beacon is at x=10, y=16",
                                       "Sensor at x=14, y=17: closest beacon is at x=10, y=16",
                                       "Sensor at x=8, y=7: closest beacon is at x=2, y=10",
                                       "Sensor at x=2, y=0: closest beacon is at x=2, y=10",
                                       "Sensor at x=0, y=11: closest beacon is at x=2, y=10",
                                       "Sensor at x=20, y=14: closest beacon is at x=25, y=17",
                                       "Sensor at x=17, y=20: closest beacon is at x=21, y=22",
                                       "Sensor at x=16, y=7: closest beacon is at x=15, y=3",
                                       "Sensor at x=14, y=3: closest beacon is at x=15, y=3",
                                       "Sensor at x=20, y=1: closest beacon is at x=15, y=3"], 20), 56000011)

run(main)
