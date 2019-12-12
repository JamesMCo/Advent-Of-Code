#!/usr/bin/env python3

#Advent of Code
#2019 Day 12, Part 1
#Solution by James C. (https://github.com/JamesMCo)

import os, sys
sys.path.append(os.path.abspath("../.."))
import unittest, util.read
from util.tests import run

from itertools import combinations

def solve(puzzle_input, steps=1000):
    class Moon:
        def __init__(self, pos):
            pos = pos.split(" ")
            self.x  = int(pos[0][3:-1])
            self.y  = int(pos[1][2:-1])
            self.z  = int(pos[2][2:-1])

            self.vx = 0
            self.vy = 0
            self.vz = 0

        def apply_grav(self, other):
            if self.x < other.x:
                self.vx  += 1
                other.vx -= 1
            elif self.x > other.x:
                self.vx  -= 1
                other.vx += 1

            if self.y < other.y:
                self.vy  += 1
                other.vy -= 1
            elif self.y > other.y:
                self.vy  -= 1
                other.vy += 1

            if self.z < other.z:
                self.vz  += 1
                other.vz -= 1
            elif self.z > other.z:
                self.vz  -= 1
                other.vz += 1

        def apply_vel(self):
            self.x += self.vx
            self.y += self.vy
            self.z += self.vz

        def calc_energy(self):
            kinetic   = sum(abs(val) for val in [self.x,  self.y,  self.z])
            potential = sum(abs(val) for val in [self.vx, self.vy, self.vz])
            return kinetic * potential

    moons = [Moon(pos) for pos in puzzle_input]
    for step in range(steps):
        for a, b in combinations(moons, 2):
            a.apply_grav(b)
        for m in moons:
            m.apply_vel()

    return sum(m.calc_energy() for m in moons)

def main():
    puzzle_input = util.read.as_lines()

    energy = solve(puzzle_input)

    print("The total energy in the system is " + str(energy) + ".")

class AOC_Tests(unittest.TestCase):
    def test_ex1(self):
        self.assertEqual(solve(["<x=-1, y=0, z=2>",
                                "<x=2, y=-10, z=-7>",
                                "<x=4, y=-8, z=8>",
                                "<x=3, y=5, z=-1>"], 10), 179)

    def test_ex2(self):
        self.assertEqual(solve(["<x=-8, y=-10, z=0>",
                                "<x=5, y=5, z=10>",
                                "<x=2, y=-7, z=3>",
                                "<x=9, y=-8, z=-3>"], 100), 1940)

run(main)
