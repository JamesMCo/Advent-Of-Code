#!/usr/bin/env python3

#Advent of Code
#2019 Day 17, Part 2
#Solution by James C. (https://github.com/JamesMCo)

import os, sys
sys.path.append(os.path.abspath("../.."))
import unittest, util.read
from util.tests import run

from functools import reduce
from util.two_d_world import World
from util.intcode_2019 import Instruction, IntcodeComputer

def solve(puzzle_input):
    computer = IntcodeComputer().load_memory(puzzle_input)
    grid = World(".", True)

    computer.memory[0] = 2

    def neighbours(x, y):
        yield from [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)]

    def is_scaffolding(cell):
        return grid[cell] != "."

    def forwards(cell, direction):
        match direction:
            case "^": return cell[0],     cell[1] - 1
            case "v": return cell[0],     cell[1] + 1
            case "<": return cell[0] - 1, cell[1]
            case ">": return cell[0] + 1, cell[1]

    def forwards_until_stopped(cell, direction):
        moves = 0
        current_cell = cell
        seen = {current_cell}
        while is_scaffolding(forwards(current_cell, direction)): # The current cell can see scaffolding in front of it
            current_cell = forwards(current_cell, direction)
            moves += 1
            seen.add(current_cell)
        return ["1"] * moves, current_cell, seen

    def rotate_to_face(start_x, start_y, direction, end_x, end_y):
        if start_y > end_y:
            # Need to face up
            match direction:
                case "^": return [],         "^"
                case "v": return ["L", "L"], "^"
                case "<": return ["R"],      "^"
                case ">": return ["L"],      "^"
        elif start_y < end_y:
            # Need to face down
            match direction:
                case "^": return ["L", "L"], "v"
                case "v": return [],         "v"
                case "<": return ["L"],      "v"
                case ">": return ["R"],      "v"
        elif start_x > end_x:
            # Need to face left
            match direction:
                case "^": return ["L"],      "<"
                case "v": return ["R"],      "<"
                case "<": return [],         "<"
                case ">": return ["L", "L"], "<"
        elif start_x < end_x:
            # Need to face right
            match direction:
                case "^": return ["R"],      ">"
                case "v": return ["L"],      ">"
                case "<": return ["L", "L"], ">"
                case ">": return [],         ">"

    while len(computer.outputs) < 2 or computer.outputs[-2:] != [10, 10]:
        # First map output is followed by two newlines
        computer.step()

    grid.load_from_lists("".join(map(chr, computer.outputs)).split("\n"))
    start, start_direction = None, None
    total_scaffolding = 0
    for cell in grid.keys():
        if grid[cell] == "#":
            total_scaffolding += 1
        elif grid[cell] in "^v<>":
            total_scaffolding += 1
            start, start_direction = cell, grid[cell]
            grid[cell] = "#"

    def explore(position, direction, instructions, walked_cells):
        if len(walked_cells) == total_scaffolding:
            return instructions

        neighbouring_scaffolding = list(filter(is_scaffolding, neighbours(*position)))
        unseen_neighbours = [neighbour for neighbour in neighbouring_scaffolding if neighbour not in walked_cells]
        if len(unseen_neighbours) > 1:
            raise RuntimeError("Not expecting to reach a T junction")
        elif len(unseen_neighbours) == 1:
            neighbour = unseen_neighbours[0]
            # Rotate to face the neighbouring cell
            rotation_instructions, new_direction = rotate_to_face(*position, direction, *neighbour)
            # Walk forwards in that direction until not able to walk forwards any further
            forwards_instructions, destination, forwards_seen = forwards_until_stopped(position, new_direction)
            return explore(destination, new_direction, instructions + rotation_instructions + forwards_instructions, walked_cells | forwards_seen)
        else:
            return None

    path = explore(start, start_direction, [], {start})

    def collapse_path(existing_path, next_elem):
        if not existing_path:
            return [next_elem]
        else:
            if existing_path[-1] in "LR" or next_elem in "LR":
                return existing_path + [next_elem]
            else:
                return existing_path[:-1] + [str(int(existing_path[-1]) + int(next_elem))]

    path = reduce(collapse_path, path, [])

    # Function-version of path found manually
    return computer.queue_inputs(map(ord, "\n".join([
        # Main
        "A,B,A,C,B,A,C,A,C,B",
        # A
        "L,12,L,8,L,8",
        # B
        "L,12,R,4,L,12,R,6",
        # C
        "R,4,L,12,L,12,R,6",
        # Continuous video feed
        "n\n"
    ]))).run().outputs[-1]

def main():
    puzzle_input = util.read.as_int_list(",")

    dust = solve(puzzle_input)

    print("The amount of dust collected is " + str(dust) + ".")

class AOC_Tests(unittest.TestCase):
    @unittest.skip("No test cases")
    def test_ex1(self):
        pass

run(main)
