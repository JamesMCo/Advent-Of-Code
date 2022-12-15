#!/usr/bin/env python3

#Advent of Code
#2022 Day 15, Part 1
#Solution by James C. (https://github.com/JamesMCo)

import os, sys
sys.path.append(os.path.abspath("../.."))
import unittest, util.read
from util.tests import run

import re
from util.two_d_world import manhattan_distance

def solve(puzzle_input, target_row=2000000):
    def count_ranges(ranges):
        ranges.sort(key=lambda x: x[0])
        combined_ranges = [ranges[0]]
        for lower, upper in ranges[1:]:
            if combined_ranges[-1][0] <= lower <= combined_ranges[-1][1]:
                if combined_ranges[-1][1] < upper:
                    # This range extends the previous range (lower is within, upper is greater than)
                    combined_ranges[-1] = (combined_ranges[-1][0], upper)
                # Otherwise, the range is fully contained by the previous range, so we don't need to do anything
            else:
                # No intersection with previous range
                combined_ranges.append((lower, upper))

        return sum(upper + 1 - lower for lower, upper in combined_ranges)

    ranges = []
    for line in puzzle_input:
        sensor_x, sensor_y, beacon_x, beacon_y = [int(x) for x in re.match("Sensor at x=(-?\d+), y=(-?\d+): closest beacon is at x=(-?\d+), y=(-?\d+)", line).groups()]

        distance = manhattan_distance(sensor_x, sensor_y, beacon_x, beacon_y)
        half_width = distance - abs(target_row - sensor_y)
        if half_width >= 0:
            if beacon_y == target_row and beacon_x == sensor_x:
                # Beacon is directly above/below the sensor, so the range will only contain a beacon
                # (i.e. range contains no spaces that cannot contain a beacon)
                continue
            elif beacon_y == target_row and beacon_x == sensor_x - half_width:
                # Beacon is at the left of the range, so shift left of range in by one to miss it out
                ranges.append((sensor_x - half_width + 1, sensor_x + half_width))
            elif beacon_y == target_row and beacon_x == sensor_x + half_width:
                # Beacon is at the right of the range, so shift right of range in by one to miss it out
                ranges.append((sensor_x - half_width, sensor_x + half_width - 1))
            else:
                # Beacon is not in the range, so range can be full possible width
                ranges.append((sensor_x - half_width, sensor_x + half_width))

    return count_ranges(ranges)

def main():
    puzzle_input = util.read.as_lines()

    empty = solve(puzzle_input)

    print("The number of positions in the target row that cannot contain a beacon is " + str(empty) + ".")

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
                                       "Sensor at x=20, y=1: closest beacon is at x=15, y=3"], 10), 26)

run(main)
