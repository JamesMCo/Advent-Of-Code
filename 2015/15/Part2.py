#!/usr/bin/env python3

#Advent of Code
#2015 Day 15, Part 2
#Solution by James C. (https://github.com/JamesMCo)

import os, sys
sys.path.append(os.path.abspath("../.."))
import unittest, util.read
from util.tests import run

def solve(puzzle_input):
    ingredients = []
    for ingredient in puzzle_input:
        ingredient = ingredient.split()
        ingredients.append([int(x) for x in [ingredient[2][:-1], ingredient[4][:-1], ingredient[6][:-1], ingredient[8][:-1], ingredient[10]]])

    def score(amounts):
        running = []
        for i in range(4):
            working = 0
            for j, amount in enumerate(amounts):
                working += amount * ingredients[j][i]
            if working < 0:
                running.append(0)
            else:
                running.append(working)

        working = 1
        for val in running:
            working *= val
        return working

    def valid(amounts):
        running = 0
        for i, amount in enumerate(amounts):
            running += amount * ingredients[i][4]
        return running == 500

    def increment(quant_list):
        i = len(quant_list) - 1
        while i >= 0:
            quant_list[i] += 1
            if quant_list[i] == 101:
                quant_list[i] = 0
                i -= 1
            else:
                break
        return quant_list

    highest = 0
    quants = [0 for x in range(len(ingredients))]
    end_state = [100 for x in range(len(ingredients))]
    while True:
        must_run = True
        while sum(quants) != 100 or must_run:
            must_run = False
            quants = increment(quants)
            if quants == end_state:
                return highest
        if valid(quants):
            temp = score(quants)
            if temp > highest:
                highest = temp

def main():
    puzzle_input = util.read.as_lines()

    highest = solve(puzzle_input)

    print("The total score of the highest-scoring cookie is " + str(highest) + ".")

class AOC_Tests(unittest.TestCase):
    def test_ex1(self):
        return self.assertEqual(solve(["Butterscotch: capacity -1, durability -2, flavor 6, texture 3, calories 8",
                                       "Cinnamon: capacity 2, durability 3, flavor -2, texture -1, calories 3"]), 57600000)

if __name__ == "__main__":
    run(main)
