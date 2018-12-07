#!/usr/bin/env python3

#Advent of Code
#Day 12, Part 2
#Solution by James C. (https://github.com/JamesMCo)

import os, sys
sys.path.append(os.path.abspath("../.."))
import unittest
from util.tests import run

def solve(puzzle_input):
    programs = {}

    def getProgramById(pName):
        if pName in programs:
            return programs[pName]
        else:
            return Program(pName)

    class Program:
        def __init__(self, pName, neighbours):
            self.pName = pName
            self.neighbours = neighbours
            self.group = None
            self.updating = False

            programs[pName] = self

        def updateNeighbours(self):
            self.updating = True

            for pName in self.neighbours:
                neighbour = getProgramById(pName)
                if not neighbour.updating and neighbour.group != self.group:
                    neighbour.group = self.group
                    neighbour.updateNeighbours()

            self.updating = False

    for p in puzzle_input:
        Program(p.split(" ")[0], " ".join(p.split(" ")[2:]).split(", "))

    i = 1
    for pName in programs:
        p = getProgramById(pName)
        if p.group == None:
            p.group = i
            p.updateNeighbours()
            i += 1

    return len(set(x.group for x in programs.values()))

def main():
    f = open("puzzle_input.txt")
    puzzle_input = f.read()[:-1].split("\n")
    f.close()

    groups = solve(puzzle_input)

    print("The number of groups in the input is " + str(groups) + ".")

class AOC_Tests(unittest.TestCase):
    def test_ex1(self):
        self.assertEqual(solve(["0 <-> 2",
                                "1 <-> 1",
                                "2 <-> 0, 3, 4",
                                "3 <-> 2, 4",
                                "4 <-> 2, 3, 6",
                                "5 <-> 6",
                                "6 <-> 4, 5"]), 2)

run(main)
