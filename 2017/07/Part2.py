#!/usr/bin/env python3

#Advent of Code
#Day 7, Part 2
#Solution by James C. (https://github.com/JamesMCo)

import os, sys
sys.path.append(os.path.abspath("../.."))
import unittest
from util.tests import run

programs = {}

class Program:
    def __init__(self, name, weight=None, children=[]):
        global programs

        self.name = name
        self.weight = weight
        self.children = children
        self.parent = None
        self.carrying = 0

        programs[name] = self

    def calcCarrying(self):
        global programs

        if self.children == []:
            return self.weight
        else:
            return sum(programs[p].calcCarrying() for p in self.children) + self.weight

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
            base = p
            break

    prev_good = 0
    while True:
        weights = []
        counts = {}
        for c in programs[base].children:
            weights.append(programs[c].calcCarrying())
            if programs[c].calcCarrying() not in counts:
                counts[programs[c].calcCarrying()] = 1
            else:
                counts[programs[c].calcCarrying()] += 1
        if len(counts) != 1:
            for c in sorted(counts, reverse=True):
                if counts[c] == 1:
                    base = programs[base].children[weights.index(c)]
                else:
                    prev_good = c
        else:
            return programs[base].weight - (programs[base].calcCarrying() - prev_good)

def main():
    f = open("puzzle_input.txt")
    puzzle_input = f.read()[:-1].split("\n")
    f.close()

    new_weight = solve(puzzle_input)

    print("The new weight would be " + str(new_weight) + ".")

class AOC_Tests(unittest.TestCase):
    def test_ex1(self):
        self.assertEqual(solve(["pbga (66)", "xhth (57)", "ebii (61)",
                                "havc (66)", "ktlj (57)", "fwft (72) -> ktlj, cntj, xhth",
                                "qoyq (66)", "padx (45) -> pbga, havc, qoyq",
                                "tknk (41) -> ugml, padx, fwft", "jptl (61)",
                                "ugml (68) -> gyxo, ebii, jptl", "gyxo (61)",
                                "cntj (57)"]), 60)

    def tearDown(self):
        global programs

        for p in list(programs.keys()):
            del programs[p]
        programs = {}

run(main)
