#!/usr/bin/env python3

#Advent of Code
#2016 Day 10, Part 2
#Solution by James C. (https://github.com/JamesMCo)

import os, sys
sys.path.append(os.path.abspath("../.."))
import unittest, util.read
from util.tests import run

botList = {}
outList = {}

def solve(puzzle_input):
    class Bot:
        def __init__(self, name, output=False):
            self.inventory = []
            self.name = name
            if not output:
                global botList
                botList[self.getName()] = self
            else:
                global outList
                outList[self.getName()] = self

        def accepting_instructions(self):
            return len(self.inventory) == 2

        def getName(self):
            return self.name

        def give(self, other, value):
            if value == "high":
                other.take(self.inventory.pop())
            else:
                other.take(self.inventory.pop(0))

        def take(self, value):
            self.inventory.append(int(value))
            self.inventory.sort()

    def getBotById(id):
        if id in botList:
            return botList[id]
        else:
            return Bot(id)

    def getOutputById(id):
        if id in outList:
            return outList[id]
        else:
            return Bot(id, True)

    while len(puzzle_input) != 0:
        i = 0
        while i < len(puzzle_input):
            j = puzzle_input[i]
            if j.split(" ")[0] == "value":
                getBotById(j.split(" ")[-1]).take(j.split(" ")[1])
                puzzle_input.pop(i)
                i = -1
            elif j.split(" ")[0] == "bot":
                if getBotById(j.split(" ")[1]).accepting_instructions():
                    low, high = None, None
                    if j.split(" ")[5] == "bot":
                        low = getBotById(j.split(" ")[6])
                    else:
                        low = getOutputById(j.split(" ")[6])
                    if j.split(" ")[-2] == "bot":
                        high = getBotById(j.split(" ")[-1])
                    else:
                        high = getOutputById(j.split(" ")[-1])
                    if not low.accepting_instructions() and not high.accepting_instructions():
                        getBotById(j.split(" ")[1]).give(low, "low")
                        getBotById(j.split(" ")[1]).give(high, "high")
                        puzzle_input.pop(i)
                        i = -1
            i += 1

    return getOutputById("0").inventory[0] * getOutputById("1").inventory[0] * getOutputById("2").inventory[0]

def main():
    puzzle_input = util.read.as_lines()

    mult_values = solve(puzzle_input)

    print("The multiplied values of the microchips in the output bins equal " + str(mult_values) + ".")

class AOC_Tests(unittest.TestCase):
    @unittest.skip("No test cases")
    def test_ex1(self):
        pass

if __name__ == "__main__":
    run(main)
