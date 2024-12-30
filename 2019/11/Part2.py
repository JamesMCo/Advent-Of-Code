#!/usr/bin/env python3

#Advent of Code
#2019 Day 11, Part 2
#Solution by James C. (https://github.com/JamesMCo)

import os, sys
sys.path.append(os.path.abspath("../.."))
import unittest, util.read
from util.tests import run

from util.two_d_world import World
from util.intcode_2019 import IntcodeComputer

def solve(puzzle_input):
    def walk(robot, current_colour):
        robot.queue_inputs(current_colour)

        while not robot.halted and len(robot.outputs) != 2:
            robot.step()

        if robot.halted:
            return [0, 0]
        results = robot.outputs.copy()
        robot.outputs.clear()
        return results

    i = IntcodeComputer().load_memory(puzzle_input)
    hull = World(0, True)
    hull[(0, 0)] = 1
    x, y = (0, 0)
    direction = "u"

    while True:
        new_colour, turn = walk(i, hull[(x, y)])
        if i.halted:
            break
        
        hull[(x, y)] = new_colour
        if new_colour == 1:
            hull.min_x = min(x, hull.min_x)
            hull.max_x = max(x, hull.max_x)
            hull.min_y = min(y, hull.min_y)
            hull.max_y = max(y, hull.max_y)

        match turn, direction:
            case (0, "u"): direction = "l"
            case (0, "d"): direction = "r"
            case (0, "l"): direction = "d"
            case (0, "r"): direction = "u"
            case (1, "u"): direction = "r"
            case (1, "d"): direction = "l"
            case (1, "l"): direction = "u"
            case (1, "r"): direction = "d"

        match direction:
            case "u": y -= 1
            case "d": y += 1
            case "l": x -= 1
            case "r": x += 1

    def hull_paint(panel):
        match panel:
            case 0: return " "
            case 1: return "█"
    return hull.pprint_custom(" ", hull_paint)

def main():
    puzzle_input = util.read.as_int_list(",")

    reg = solve(puzzle_input)

    print("The registration identifier is:\n" + reg)

class AOC_Tests(unittest.TestCase):
    @unittest.skip("No test cases")
    def test_ex1(self):
        pass

if __name__ == "__main__":
    run(main)
