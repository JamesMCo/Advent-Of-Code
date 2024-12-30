#!/usr/bin/env python3

#Advent of Code
#2016 Day 8, Part 1
#Solution by James C. (https://github.com/JamesMCo)

import os, sys
sys.path.append(os.path.abspath("../.."))
import unittest, util.read
from util.tests import run

def solve(puzzle_input):
    d = [["." for i in range(50)] for x in range(6)]

    def rect(s, d):
        w, h = s.split("x")
        w = int(w)
        h = int(h)
        for x in range(w):
            for y in range(h):
                d[y][x] = "#"
        return d

    def rotate(roc, n, a, d):
        if roc == "row":
            cur = "".join(d[int(n)]) + "".join(d[int(n)])
            if int(a) > 0:
                cur = cur[50-int(a):100-int(a)]
            else:
                cur = cur[int(a):50+int(a)]
            d[int(n)] = list(cur)
        else:
            cur = ""
            for row in d:
                cur += row[int(n)]
            cur += cur
            if int(a) > 0:
                cur = cur[6-int(a):12-int(a)]
            else:
                cur = cur[int(a):6+int(a)]
            for p in range(len(cur)):
                d[p][int(n)] = cur[p]
        return d

    def printd(d):
        for row in d:
            print("".join(row))

    for inst in puzzle_input:
        if inst.split(" ")[0] == "rect":
            d = rect(inst.split(" ")[1], d)
        elif inst.split(" ")[0] == "rotate":
            d = rotate(inst.split(" ")[1], inst.split(" ")[2].split("=")[1], inst.split(" ")[4], d)

    lit = 0
    for i in d:
        for x in i:
            if x == "#":
                lit += 1

    return lit

def main():
    puzzle_input = util.read.as_lines()

    lit = solve(puzzle_input)

    print("The number of lit pixels is " + str(lit) + ".")

class AOC_Tests(unittest.TestCase):
    @unittest.skip("No test cases")
    def test_ex1(self):
        pass

if __name__ == "__main__":
    run(main)
