#!/usr/bin/env python3

#Advent of Code
#2022 Day 22, Part 1
#Solution by James C. (https://github.com/JamesMCo)

import os, sys
sys.path.append(os.path.abspath("../.."))
import unittest, util.read
from util.tests import run

import re
from util.two_d_world import World

def solve(puzzle_input):
    board = World(" ", ddict=True)
    board.load_from_lists(puzzle_input[:puzzle_input.index("")], origin=(-1, -1))
    instructions = re.findall(r"(\d+|[LR])", puzzle_input[puzzle_input.index("") + 1])

    def try_to_move(start_x, start_y, facing):
        offset_x = offset_y = 0
        match facing:
            case 0: offset_x = 1
            case 1: offset_y = 1
            case 2: offset_x = -1
            case 3: offset_y = -1

        if board[(start_x + offset_x, start_y + offset_y)] != " ":
            # Don't need to wrap
            if board[(start_x + offset_x, start_y + offset_y)] != "#":
                return (start_x + offset_x, start_y + offset_y)
            else:
                return (start_x, start_y)
        else:
            # Wrap to other side
            new_x, new_y = start_x, start_y
            while board[(new_x, new_y)] != " ":
                new_x -= offset_x
                new_y -= offset_y
            
            if board[(new_x + offset_x, new_y + offset_y)] != "#":
                return (new_x + offset_x, new_y + offset_y)
            else:
                # If after wrapping you'd hit a wall, don't move from original non-wrapped location
                return (start_x, start_y)
    
    x = min(i + 1 for i, cell in enumerate(puzzle_input[0]) if cell != " ")
    y = 1
    facing = 0

    for instruction in instructions:
        match instruction:
            case distance if distance.isdecimal():
                distance = int(distance)
                for step in range(distance):
                    next_x, next_y = try_to_move(x, y, facing)
                    if (x, y) == (next_x, next_y):
                        # Can't move, so stop
                        break
                    x, y = next_x, next_y
            case "L" if facing == 0:
                facing = 3
            case "L":
                facing -= 1
            case "R" if facing == 3:
                facing = 0
            case "R":
                facing += 1

    return (1000 * y) + (4 * x) + facing

def main():
    puzzle_input = util.read.as_lines_only_rstrip()

    password = solve(puzzle_input)

    print("The final password is " + str(password) + ".")

class AOC_Tests(unittest.TestCase):
    def test_ex1(self):
        return self.assertEqual(solve(["        ...#",
                                       "        .#..",
                                       "        #...",
                                       "        ....",
                                       "...#.......#",
                                       "........#...",
                                       "..#....#....",
                                       "..........#.",
                                       "        ...#....",
                                       "        .....#..",
                                       "        .#......",
                                       "        ......#.",
                                       "",
                                       "10R5L5R10L4R5L5"]), 6032)

if __name__ == "__main__":
    run(main)
