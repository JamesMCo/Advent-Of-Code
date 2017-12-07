#!/usr/bin/env python3

#Advent of Code
#Day 7, Part 2
#Solution by James C. (https://github.com/JamesMCo)

import unittest

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

    def getName(self):
        return self.name

    def getWeight(self):
        return self.weight

    def setWeight(self, weight):
        self.weight = weight

    def getChildren(self):
        return self.children

    def setChildren(self, children):
        self.children = children

    def getParent(self):
        return self.parent

    def setParent(self, other):
        self.parent = other

    def getCarrying(self):
        global programs

        if self.children == []:
            return self.weight
        else:
            return sum(programs[p].getCarrying() for p in self.children) + self.weight

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
        p.setWeight(int(w[1][1:-1]))
        if len(w) > 2:
            p.setChildren([x.replace(",", "") for x in w[3:]])

    for p in programs:
        if programs[p].getChildren() != []:
            for c in programs[p].getChildren():
                programs[c].setParent(p)

    for p in programs:
        if programs[p].getParent() == None:
            base = p
            break

    prev_good = 0
    while True:
        weights = []
        counts = {}
        for c in programs[base].getChildren():
            weights.append(programs[c].getCarrying())
            if programs[c].getCarrying() not in counts:
                counts[programs[c].getCarrying()] = 1
            else:
                counts[programs[c].getCarrying()] += 1
        if len(counts) != 1:
            for c in sorted(counts, reverse=True):
                if counts[c] == 1:
                    base = programs[base].getChildren()[weights.index(c)]
                else:
                    prev_good = c
        else:
            return programs[base].getWeight() - (programs[base].getCarrying() - prev_good)

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

if __name__ == "__main__":
    if unittest.main(verbosity=2, exit=False).result.wasSuccessful():
        main()
        exit(0)
    else:
        exit(1)
