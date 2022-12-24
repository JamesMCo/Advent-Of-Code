#!/usr/bin/env python3

#Advent of Code
#2022 Day 24, Part 2
#Solution by James C. (https://github.com/JamesMCo)

import os, sys
sys.path.append(os.path.abspath("../.."))
import unittest, util.read
from util.tests import run

from collections import deque
from math import inf, lcm

def solve(puzzle_input):
    # (0, 0) is the top left of the map inside the walls
    # (i.e. the left walls are at x=-1, the top walls are at y=-1)

    start = (puzzle_input[0].index(".") - 1, -1)
    end   = (puzzle_input[-1].index(".") - 1, len(puzzle_input) - 2)

    min_x = 0
    max_x = len(puzzle_input[0]) - 3
    min_y = 0
    max_y = len(puzzle_input) - 3

    # All <> blizzards will be in their original location after they have moved the number of steps equal to the width of the map
    # All ^v blizzards will be in their original location after they have moved the number of steps equal to the height of the map
    # Therefore all blizzards will be in their original location after the lowest common multiple of the width and height of the map
    cycle_length = lcm(max_x + 1, max_y + 1)

    blizzards = {}
    for y, row in enumerate(puzzle_input[min_y:max_y+2]):
        for x, col in enumerate(row[min_x:max_x+2]):
            match col:
                case ".": pass
                case "#": pass
                case blizzard: blizzards[(x-1, y-1)] = blizzard

    def in_bounds(x, y):
        return (x, y) in [start, end] or (min_x <= x <= max_x and min_y <= y <= max_y)

    def is_blizzard(minute, x, y):
        if ((x-minute) % (max_x+1), y) in blizzards and blizzards[((x-minute) % (max_x+1), y)] == ">":
            return True
        elif (x, (y-minute) % (max_y+1)) in blizzards and blizzards[(x, (y-minute) % (max_y+1))] == "v":
            return True
        elif ((x+minute) % (max_x+1), y) in blizzards and blizzards[((x+minute) % (max_x+1), y)] == "<":
            return True
        elif (x, (y+minute) % (max_y+1)) in blizzards and blizzards[(x, (y+minute) % (max_y+1))] == "^":
            return True
        else:
            return False

    def get_next_coords(minute, x, y):
        results = []
        if in_bounds(x+1, y) and not is_blizzard(minute+1, x+1, y):
            results.append((x+1, y))
        if in_bounds(x, y+1) and not is_blizzard(minute+1, x, y+1):
            results.append((x, y+1))
        if in_bounds(x-1, y) and not is_blizzard(minute+1, x-1, y):
            results.append((x-1, y))
        if in_bounds(x, y-1) and not is_blizzard(minute+1, x, y-1):
            results.append((x, y-1))
        if in_bounds(x, y) and not is_blizzard(minute+1, x, y):
            results.append((x, y))
        return results

    def find_shortest_path(start_coords, end_coords, start_minute):
        states = deque([(start_minute, start_coords)])
        seen_states = set()
        shortest = inf
        while states:
            minute, coords = states.popleft()
            seen_states.add((minute, coords))

            if coords == end_coords:
                return minute

            for next_coords in get_next_coords(minute, *coords):
                if ((minute+1) % cycle_length, next_coords) not in seen_states and (minute+1, next_coords) not in states:
                    states.append((minute+1, next_coords))
        return shortest

    stage_one   = find_shortest_path(start, end, 0)
    stage_two   = find_shortest_path(end, start, stage_one)
    stage_three = find_shortest_path(start, end, stage_two)

    return stage_three

def main():
    puzzle_input = util.read.as_lines()

    steps = solve(puzzle_input)

    print("The fewest number of minutes required to reach the goal, go back to the start, then reach the goal again is " + str(steps) + ".")

class AOC_Tests(unittest.TestCase):
    def test_ex1(self):
        return self.assertEqual(solve(["#.######",
                                       "#>>.<^<#",
                                       "#.<..<<#",
                                       "#>v.><>#",
                                       "#<^v^^>#",
                                       "######.#"]), 54)

run(main)
