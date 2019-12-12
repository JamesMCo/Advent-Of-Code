#!/usr/bin/env python3

#Advent of Code
#2019 Day 12, Part 2
#Solution by James C. (https://github.com/JamesMCo)

import os, sys
sys.path.append(os.path.abspath("../.."))
import unittest, util.read
from util.tests import run

from itertools import combinations
from math import gcd

def solve(puzzle_input):
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

    def xs(moons):
        return (moons[0].x,  moons[1].x,  moons[2].x,  moons[3].x,
                moons[0].vx, moons[1].vx, moons[2].vx, moons[3].vx)
    def ys(moons):
        return (moons[0].y,  moons[1].y,  moons[2].y,  moons[3].y,
                moons[0].vy, moons[1].vy, moons[2].vy, moons[3].vy)
    def zs(moons):
        return (moons[0].z,  moons[1].z,  moons[2].z,  moons[3].z,
                moons[0].vz, moons[1].vz, moons[2].vz, moons[3].vz)

    moons = [Moon(pos) for pos in puzzle_input]

    x_states = {xs(moons): 0}
    y_states = {ys(moons): 0}
    z_states = {zs(moons): 0}

    cycle_x  = None
    cycle_y  = None
    cycle_z  = None

    step = 0
    while cycle_x == None or cycle_y == None or cycle_z == None:
        for a, b in combinations(moons, 2):
            a.apply_grav(b)
        for m in moons:
            m.apply_vel()
        step += 1

        if cycle_x == None:
            if xs(moons) in x_states:
                cycle_x = step - x_states[xs(moons)]
            x_states[xs(moons)] = step
        if cycle_y == None:
            if ys(moons) in y_states:
                cycle_y = step - y_states[ys(moons)]
            y_states[ys(moons)] = step
        if cycle_z == None:
            if zs(moons) in z_states:
                cycle_z = step - z_states[zs(moons)]
            z_states[zs(moons)] = step
    
    lcm = lambda a, b: int((a * b)/gcd(a, b))
    return lcm(cycle_x, lcm(cycle_y, cycle_z))

def main():
    puzzle_input = util.read.as_lines()

    steps = solve(puzzle_input)

    print("The number of steps it takes to reach a repeated state is " + str(steps) + ".")

class AOC_Tests(unittest.TestCase):
    def test_ex1(self):
        self.assertEqual(solve(["<x=-1, y=0, z=2>",
                                "<x=2, y=-10, z=-7>",
                                "<x=4, y=-8, z=8>",
                                "<x=3, y=5, z=-1>"]), 2772)

    def test_ex2(self):
        self.assertEqual(solve(["<x=-8, y=-10, z=0>",
                                "<x=5, y=5, z=10>",
                                "<x=2, y=-7, z=3>",
                                "<x=9, y=-8, z=-3>"]), 4686774924)

run(main)
