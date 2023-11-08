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

    def check_valid_c_program(program, c_count):
        c_start = 0
        while program[c_start] in "AB":
            c_start += 1
        c_str = ",".join(program[c_start:c_start + c_count])

        program_str = ",".join(program)
        while c_str in program_str:
            program_str = program_str.replace(c_str, "C")

        if all([char in "ABC," for char in program_str]):
            return c_str
        else:
            return False

    def check_valid_program(program, a_count, b_count, b_start_offset):
        program_str = ",".join(program)
        a_str = ",".join(path[:a_count])
        b_str = ",".join(path[a_count + b_start_offset:a_count + b_start_offset + b_count])

        while a_str in program_str:
            program_str = program_str.replace(a_str, "A")

        while b_str in program_str:
            program_str = program_str.replace(b_str, "B")

        for c_count in range(1, 11):
            # input(f"{a_count=} {b_count=} {b_offset=} {c_count=}")
            if c_str := check_valid_c_program(program_str.split(","), c_count):
                while c_str in program_str:
                    program_str = program_str.replace(c_str, "C")
                return program_str, a_str, b_str, c_str

        return None

    # Function finding worked out after reading various threads on /r/AdventOfCode
    # With a 20-character limit, each function can be at most 10 instructions
    # (1 character followed by 1 comma)
    for a_len in range(1, 11):
        if len(",".join(path[:a_len])) > 20:
            break
        for b_len in range(1, 11):
            # The final program might not be of the form AB, and so there may be
            # something between A and B. It too can't be longer than 10 instructions.
            for b_offset in range(0, 11):
                if len(",".join(path[a_len:a_len + b_len])) > 20:
                    break
                # c_len follows as a result of a_len and b_len

                result = check_valid_program(path, a_len, b_len, b_offset)
                if result:
                    return computer\
                        .queue_inputs("\n".join(result) + "\n")\
                        .queue_inputs("n\n")\
                        .run().outputs[-1]

def main():
    puzzle_input = util.read.as_int_list(",")

    dust = solve(puzzle_input)

    print("The amount of dust collected is " + str(dust) + ".")

class AOC_Tests(unittest.TestCase):
    @unittest.skip("No test cases")
    def test_ex1(self):
        pass

run(main)
