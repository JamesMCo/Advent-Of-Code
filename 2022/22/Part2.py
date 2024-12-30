#!/usr/bin/env python3

#Advent of Code
#2022 Day 22, Part 2
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

    def wrap(x, y, facing):
        # x and y are positions within the net
        # Returns x, y, and facing for a location one cell outside the net
        # (i.e. such that looking one space forwards will result in the
        # position after moving once from the original location observing
        # cube wrapping rules)

        # Faces are labelled as follows:
        #  12
        #  3
        # 45
        # 6
        # Directions are all relative to the original map (i.e. 1 is up from 3)

        # Face 1
        # Wraps on the top to the left of face 6 (facing up becomes right)
        # Wraps on the left to the left of face 4 (facing left becomes right)
        if y == 1 and 51 <= x <= 100 and facing == 3:
            # Top face
            return (0, 151 + ((x - 1) - 50), 0)
        elif x == 51 and 1 <= y <= 50 and facing == 2:
            # Left face
            return (0, 150 - (y - 1), 0)

        # Face 2
        # Wraps on the top to the bottom of face 6 (facing up becomes up)
        # Wraps on the right to the right of face 5 (facing right becomes left)
        # Wraps on the bottom to the right of face 3 (facing down becomes left)
        elif y == 1 and 101 <= x <= 150 and facing == 3:
            # Top face
            return (1 + ((x - 1) - 100), 201, 3)
        elif x == 150 and 1 <= y <= 51 and facing == 0:
            # Right face
            return (101, 150 - (y - 1), 2)
        elif y == 50 and 101 <= x <= 150 and facing == 1:
            # Bottom face
            return (101, 51 + ((x - 1) - 100), 2)

        # Face 3
        # Wraps on the left to the top of face 4 (facing left becomes down)
        # Wraps on the right to the bottom of face 2 (facing right becomes up)
        elif x == 51 and 51 <= y <= 100 and facing == 2:
            # Left face
            return (1 + ((y - 1) - 50), 100, 1)
        elif x == 100 and 51 <= y <= 100 and facing == 0:
            # Right face
            return (101 + ((y - 1) - 50), 51, 3)

        # Face 4
        # Wraps on the top to the left of face 3 (facing up becomes right)
        # Wraps on the left to the left of face 1 (facing left becomes right)
        elif y == 101 and 1 <= x <= 50 and facing == 3:
            # Top face
            return (50, 51 + (x - 1), 0)
        elif x == 1 and 101 <= y <= 150 and facing == 2:
            # Left face
            return (50, 50 - ((y - 1) - 100), 0)

        # Face 5
        # Wraps on the right to the right of face 2 (facing right becomes left)
        # Wraps on the bottom to the right of face 6 (facing down becomes left)
        elif x == 100 and 101 <= y <= 150 and facing == 0:
            # Right face
            return (151, 50 - ((y - 1) - 100), 2)
        elif y == 150 and 51 <= x <= 100 and facing == 1:
            # Bottom face
            return (51, 151 + ((x - 1) - 50), 2)

        # Face 6
        # Wraps on the left to the top of face 1 (facing left becomes down)
        # Wraps on the right to the bottom of face 5 (facing right becomes up)
        # Wraps on the bottom to the top of face 2 (facing down becomes down)
        elif x == 1 and 151 <= y <= 200 and facing == 2:
            return (51 + ((y - 1) - 150), 0, 1)
        elif x == 50 and 151 <= y <= 200 and facing == 0:
            return (51 + ((y - 1) - 150), 151, 3)
        elif y == 200 and 1 <= x <= 50 and facing == 1:
            return (101 + (x - 1), 0, 1)

    def try_to_move(start_x, start_y, start_facing):
        offset_x = offset_y = 0
        match start_facing:
            case 0: offset_x = 1
            case 1: offset_y = 1
            case 2: offset_x = -1
            case 3: offset_y = -1

        if board[(start_x + offset_x, start_y + offset_y)] != " ":
            # Don't need to wrap
            if board[(start_x + offset_x, start_y + offset_y)] != "#":
                return (start_x + offset_x, start_y + offset_y, start_facing)
            else:
                return (start_x, start_y, start_facing)
        else:
            # Wrap to other side
            new_x, new_y, new_facing = wrap(start_x, start_y, start_facing)

            offset_x = offset_y = 0
            match new_facing:
                case 0: offset_x = 1
                case 1: offset_y = 1
                case 2: offset_x = -1
                case 3: offset_y = -1
            
            if board[(new_x + offset_x, new_y + offset_y)] != "#":
                return (new_x + offset_x, new_y + offset_y, new_facing)
            else:
                # If after wrapping you'd hit a wall, don't move from original non-wrapped location
                return (start_x, start_y, start_facing)
    
    x = min(i + 1 for i, cell in enumerate(puzzle_input[0]) if cell != " ")
    y = 1
    facing = 0

    for instruction in instructions:
        match instruction:
            case distance if distance.isdecimal():
                distance = int(distance)
                for step in range(distance):
                    next_x, next_y, next_facing = try_to_move(x, y, facing)
                    if (x, y) == (next_x, next_y):
                        # Can't move, so stop
                        break
                    x, y, facing = next_x, next_y, next_facing
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
    @unittest.skip("Though there is a test case in the puzzle description, it has a different shape to the puzzle input. " +\
                   "Eric Wastl has confirmed on reddit (https://www.reddit.com/r/adventofcode/comments/zsgbe7/comment/j17smus/) that all inputs have the same shape, and so my solution is hard coded to the shape of all real inputs. " +\
                   "Writing a solution that works on any potential net is left as an exercise for the reader.")
    def test_ex1(self):
        pass

if __name__ == "__main__":
    run(main)
