#!/usr/bin/env python3

#Advent of Code
#2021 Day 17, Part 1
#Solution by James C. (https://github.com/JamesMCo)

import os, sys
sys.path.append(os.path.abspath("../.."))
import unittest, util.read
from util.tests import run

from math import inf
import re

def solve(puzzle_input):
    r_x1, r_x2, r_y1, r_y2 = re.match("target area: x=(-?\d+)..(-?\d+), y=(-?\d+)..(-?\d+)", puzzle_input).groups()
    r_x1, r_x2 = sorted(int(n) for n in [r_x1, r_x2])
    r_y1, r_y2 = sorted(int(n) for n in [r_y1, r_y2])
    in_region = lambda x, y: r_x1 <= x <= r_x2 and r_y1 <= y <= r_y2
    past_region = lambda x, y, vx, vy: (x > r_x2 and vx > 0) or (y < r_y1 and vy <= 0)

    class Probe:
        def __init__(self, vx, vy):
            self.vx, self.vy = vx, vy
            self.enters_target = False
            self.highest_y = -inf

            self.simulate()

        def simulate(self):
            x, y = 0, 0
            vx, vy = self.vx, self.vy
            while not past_region(x, y, vx, vy):
                x += vx
                y += vy
                self.highest_y = max(self.highest_y, y)

                if in_region(x, y):
                    self.enters_target = True
                    break

                if   vx > 0: vx -= 1
                elif vx < 0: vx += 1
                vy -= 1
            
            self.final_x, self.final_y = x, y
            self.final_vx, self.final_vy = vx, vy

        def undershoots(self):
            return self.final_x < r_x1

        def overshoots(self):
            return past_region(self.final_x, self.final_y, self.final_vx, self.final_vy)

    # Bounds logic from various commenters on the subreddit
    # Range searched for y velocity is:
    # from: lowest point in target region
    # to:   negative of lowest point in target region + 1
    #       (when y = 0 the second time, the velocity will be the negative of the
    #       initial velocity, and then the velocity will be increased by one.
    #       the largest velocity at this point would land the probe at the bottom
    #       row of the target region. this velocity would be r_y1, and thus working
    #       backwards the initial velocity would need to be -(r_y1 + 1))

    highest_y = -inf
    vy = r_y1
    while True and vy <= -(r_y1 + 1):
        vx = -1
        targets_hit = 0
        while True:
            vx += 1
            p = Probe(vx, vy)
            if p.undershoots():
                continue
            elif p.enters_target:
                highest_y = max(highest_y, p.highest_y)
                targets_hit += 1
                continue
            elif p.overshoots():
                break
        vy += 1
    return highest_y

def main():
    puzzle_input = util.read.as_string()

    y = solve(puzzle_input)

    print("The highest y position reached on the probe's trajectory is " + str(y) + ".")

class AOC_Tests(unittest.TestCase):
    def test_ex1(self):
        return self.assertEqual(solve("target area: x=20..30, y=-10..-5"), 45)

run(main)
