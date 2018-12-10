#!/usr/bin/env python3

#Advent of Code
#2018 Day 10, Part 1
#Solution by James C. (https://github.com/JamesMCo)

import os, sys
sys.path.append(os.path.abspath("../.."))
import unittest, util.read
from util.tests import run

from math import inf

interactive = os.environ.get("TRAVIS") != "true"

def solve(puzzle_input):
    class Controller:
        def __init__(self):
            self.dots = []

        def print_grid(self):
            print()

            p = set([x.get_pos() for x in self.dots])
            left  = min(x[0] for x in p)
            right = max(x[0] for x in p)
            top   = min(x[1] for x in p)
            bot   = max(x[1] for x in p)

            for y in range(top, bot+1):
                for x in range(left, right+1):
                    if (x, y) in p:
                        print("#", end="")
                    else:
                        print(".", end="")
                print()

        def move(self):
            for dot in self.dots:
                dot.move()

        def move_until_close(self, dx, dy):
            left  = 0
            right = inf
            top   = 0
            bot   = inf

            while right - left > dx and bot - top > dy:
                self.move()

                p = set([x.get_pos() for x in self.dots])
                left  = min(x[0] for x in p)
                right = max(x[0] for x in p)
                top   = min(x[1] for x in p)
                bot   = max(x[1] for x in p)

    class Dot:
        def __init__(self, line, controller):
            self.x  = int(line.split("<")[1].split(",")[0])
            self.y  = int(line.split(">")[0].split(",")[1])
            self.dx = int(line.split("<")[2].split(",")[0])
            self.dy = int(line.split(">")[1].split(",")[1])

            controller.dots.append(self)

        def get_pos(self):
            return (self.x, self.y)

        def move(self):
            self.x += self.dx
            self.y += self.dy
    
    c = Controller()
    for line in puzzle_input:
        Dot(line, c)

    c.move_until_close(50, 50)

    i = ""
    while i == "":
        c.print_grid()
        i = input("\nType the message seen and press Enter to quit, just press Enter to iterate.\n> ")
        c.move()
    return i

def main():
    puzzle_input = util.read.as_lines()

    if interactive:
        solve(puzzle_input)
    else:
        print("Skipping running solution due to interactivity requirement")

class AOC_Tests(unittest.TestCase):
    @unittest.skipIf(not interactive, "Test cases skipped on Travis due to interactivity requirement")
    def test_ex1(self):
        self.assertEqual(solve(["position=< 9,  1> velocity=< 0,  2>",
                                "position=< 7,  0> velocity=<-1,  0>",
                                "position=< 3, -2> velocity=<-1,  1>",
                                "position=< 6, 10> velocity=<-2, -1>",
                                "position=< 2, -4> velocity=< 2,  2>",
                                "position=<-6, 10> velocity=< 2, -2>",
                                "position=< 1,  8> velocity=< 1, -1>",
                                "position=< 1,  7> velocity=< 1,  0>",
                                "position=<-3, 11> velocity=< 1, -2>",
                                "position=< 7,  6> velocity=<-1, -1>",
                                "position=<-2,  3> velocity=< 1,  0>",
                                "position=<-4,  3> velocity=< 2,  0>",
                                "position=<10, -3> velocity=<-1,  1>",
                                "position=< 5, 11> velocity=< 1, -2>",
                                "position=< 4,  7> velocity=< 0, -1>",
                                "position=< 8, -2> velocity=< 0,  1>",
                                "position=<15,  0> velocity=<-2,  0>",
                                "position=< 1,  6> velocity=< 1,  0>",
                                "position=< 8,  9> velocity=< 0, -1>",
                                "position=< 3,  3> velocity=<-1,  1>",
                                "position=< 0,  5> velocity=< 0, -1>",
                                "position=<-2,  2> velocity=< 2,  0>",
                                "position=< 5, -2> velocity=< 1,  2>",
                                "position=< 1,  4> velocity=< 2,  1>",
                                "position=<-2,  7> velocity=< 2, -2>",
                                "position=< 3,  6> velocity=<-1, -1>",
                                "position=< 5,  0> velocity=< 1,  0>",
                                "position=<-6,  0> velocity=< 2,  0>",
                                "position=< 5,  9> velocity=< 1, -2>",
                                "position=<14,  7> velocity=<-2,  0>",
                                "position=<-3,  6> velocity=< 2, -1>"]), "HI")

run(main)
