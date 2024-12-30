#!/usr/bin/env python3

#Advent of Code
#2017 Day 7, Part 1
#Solution by James C. (https://github.com/JamesMCo)

import os, sys
sys.path.append(os.path.abspath("../.."))
import unittest, util.read
from util.tests import run

programs = {}

class Program:
    def __init__(self, name, weight=None, children=[]):
        global programs

        self.name = name
        self.weight = weight
        self.children = children
        self.parent = None

        programs[name] = self

    def __str__(self):
        return "Program \"" + self.name + "\" | Weight = " + str(self.weight) + ", Children = " + str(self.children) + ", Parent = " + str(self.parent)

def getProgramById(pName):
    if pName in programs:
        return programs[pName]
    else:
        return Program(pName)

def solve(puzzle_input):
    global programs

    for l in puzzle_input:
        w = l.split(" ")
        p = getProgramById(w[0])
        p.weight = int(w[1][1:-1])
        if len(w) > 2:
            p.children = [x.replace(",", "") for x in w[3:]]

    for p in programs:
        if programs[p].children != []:
            for c in programs[p].children:
                programs[c].parent = p

    for p in programs:
        if programs[p].parent == None:
            return programs[p]

def main():
    puzzle_input = util.read.as_lines()

    base = solve(puzzle_input)

    print("The name of the bottom program is " + str(base.name) + ".")

class AOC_Tests(unittest.TestCase):
    def test_ex1(self):
        self.assertEqual(solve(["pbga (66)", "xhth (57)", "ebii (61)",
                                "havc (66)", "ktlj (57)", "fwft (72) -> ktlj, cntj, xhth",
                                "qoyq (66)", "padx (45) -> pbga, havc, qoyq",
                                "tknk (41) -> ugml, padx, fwft", "jptl (61)",
                                "ugml (68) -> gyxo, ebii, jptl", "gyxo (61)",
                                "cntj (57)"]).name, "tknk")

    def tearDown(self):
        global programs

        for p in list(programs.keys()):
            del programs[p]
        programs = {}

if __name__ == "__main__":
    run(main)
