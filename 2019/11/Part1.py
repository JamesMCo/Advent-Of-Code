#!/usr/bin/env python3

#Advent of Code
#2019 Day 11, Part 1
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
    painted = World(0, True)
    x, y = (0, 0)
    direction = "u"

    while True:
        new_colour, turn = walk(i, hull[(x, y)])
        if i.halted:
            break
        
        hull[(x, y)] = new_colour
        painted[(x, y)] = 1

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

    return sum(painted.values())

def main():
    puzzle_input = util.read.as_int_list(",")

    panels = solve(puzzle_input)

    print("The number of panels painted at least once is " + str(panels) + ".")

class AOC_Tests(unittest.TestCase):
    @unittest.skip("No test cases")
    def test_ex1(self):
        pass

if __name__ == "__main__":
    run(main)
