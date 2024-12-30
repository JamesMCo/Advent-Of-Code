#!/usr/bin/env python3

#Advent of Code
#2020 Day 21, Part 1
#Solution by James C. (https://github.com/JamesMCo)

import os, sys
sys.path.append(os.path.abspath("../.."))
import unittest, util.read
from util.tests import run

def solve(puzzle_input):
    # Based partly on a hint that was given to me by a friend (whose solution repo
    # can be found here: https://gitlab.com/Nohus/advent-of-code-2020/-/tree/master )
    # He suggested that I map from allergens to ingredients, rather than what I had
    # originally (ingredients to allergens)

    def parse(food):
        food = food[:-1].split(" (contains ")
        return (food[0].split(), food[1].split(", "))

    foods = [parse(food) for food in puzzle_input]
    all_ingredients = set.union({x for food in foods for x in food[0]})
    all_allergens   = set.union({x for food in foods for x in food[1]})
    a_to_ing_opts = {a: all_ingredients for a in all_allergens}

    for ingredients, allergens in foods:
        for allergen in allergens:
                a_to_ing_opts[allergen] = a_to_ing_opts[allergen].intersection(set(ingredients))

    maybe_has_allergen = set.union(*list(a_to_ing_opts.values()))
    cant_have_allergen = all_ingredients.difference(maybe_has_allergen)

    original_ingredients = [x for food in foods for x in food[0]]
    return sum(original_ingredients.count(ingredient) for ingredient in cant_have_allergen)

def main():
    puzzle_input = util.read.as_lines()

    ingredient_count = solve(puzzle_input)

    print("The number of times ingredients with no allergens appear is " + str(ingredient_count) + ".")

class AOC_Tests(unittest.TestCase):
    def test_ex1(self):
        return self.assertEqual(solve(["mxmxvkd kfcds sqjhc nhms (contains dairy, fish)",
                                       "trh fvjkl sbzzf mxmxvkd (contains dairy)",
                                       "sqjhc fvjkl (contains soy)",
                                       "sqjhc mxmxvkd sbzzf (contains fish)"]), 5)

if __name__ == "__main__":
    run(main)
