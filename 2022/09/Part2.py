#!/usr/bin/env python3

#Advent of Code
#2022 Day 9, Part 2
#Solution by James C. (https://github.com/JamesMCo)

import os, sys
sys.path.append(os.path.abspath("../.."))
import unittest, util.read
from util.tests import run

def solve(puzzle_input):
    class Knot:
        def __init__(self, x=0, y=0):
            self.x = x
            self.y = y

            self.visited = set([str(self)])

        def touching(self, other):
            return (other.x, other.y) in [(self.x+dx, self.y+dy) for dx in range(-1, 2) for dy in range(-1, 2)]

        def step(self, direction):
            match direction:
                case "U":
                    self.y -= 1
                case "D":
                    self.y += 1
                case "L":
                    self.x -= 1
                case "R":
                    self.x += 1
                # Diagonal cases won't occur in puzzle input,
                # but will occur when the tail catching up to the head
                case "UR":
                    self.y -= 1
                    self.x += 1
                case "DR":
                    self.y += 1
                    self.x += 1
                case "DL":
                    self.y += 1
                    self.x -= 1
                case "UL":
                    self.y -= 1
                    self.x -= 1
            self.visited.add(str(self))

        def catchup(self, other):
            if   other.x == self.x and other.y == self.y - 2:
                return self.step("U")
            elif other.x == self.x and other.y == self.y + 2:
                return self.step("D")
            elif other.x == self.x - 2 and other.y == self.y:
                return self.step("L")
            elif other.x == self.x + 2 and other.y == self.y:
                return self.step("R")

            # Head is not in the same row/column as the tail

            if other.y < self.y:
                direction = "U"
            else:
                direction = "D"

            if other.x < self.x:
                direction += "L"
            else:
                direction += "R"

            return self.step(direction)

        def __str__(self):
            return str((self.x, self.y))

    class Rope:
        def __init__(self, instructions):
            self.knots = [Knot() for knot in range(10)]
            self.head  = self.knots[0]
            self.tail  = self.knots[-1]

            self.instructions = [(instruction.split()[0], int(instruction.split()[1])) for instruction in instructions]

        def run(self):
            for direction, steps in self.instructions:
                for step in range(steps):
                    self.head.step(direction)
                    for ahead, behind in zip(self.knots, self.knots[1:]):
                        if not ahead.touching(behind):
                            behind.catchup(ahead)

    rope = Rope(puzzle_input)
    rope.run()

    return len(rope.tail.visited)

def main():
    puzzle_input = util.read.as_lines()

    positions = solve(puzzle_input)

    print("The number of positions that the tail of the rope visits at least once is " + str(positions) + ".")

class AOC_Tests(unittest.TestCase):
    def test_ex1(self):
        return self.assertEqual(solve(["R 4",
                                       "U 4",
                                       "L 3",
                                       "D 1",
                                       "R 4",
                                       "D 1",
                                       "L 5",
                                       "R 2"]), 1)

    def test_ex2(self):
        return self.assertEqual(solve(["R 5",
                                       "U 8",
                                       "L 8",
                                       "D 3",
                                       "R 17",
                                       "D 10",
                                       "L 25",
                                       "U 20"]), 36)

if __name__ == "__main__":
    run(main)
