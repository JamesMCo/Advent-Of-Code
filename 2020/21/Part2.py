#!/usr/bin/env python3

#Advent of Code
#2020 Day 21, Part 2
#Solution by James C. (https://github.com/JamesMCo)

import os, sys
sys.path.append(os.path.abspath("../.."))
import unittest, util.read
from util.tests import run

def solve(puzzle_input):
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
    final_mapping = {}

    while True:
        cont = False
        for a in a_to_ing_opts:
            if a not in final_mapping and len(a_to_ing_opts[a]) == 1:
                (final_mapping[a],) = a_to_ing_opts[a]
                for other in a_to_ing_opts:
                    if other != a:
                        a_to_ing_opts[other].discard(final_mapping[a])
                cont = True
        if not cont:
            break

    return ",".join(final_mapping[a] for a in sorted(all_allergens))

def main():
    puzzle_input = util.read.as_lines()

    canonical_dangerous_ingredient_list = solve(puzzle_input)

    print("The canonical dangerous ingredient list is " + str(canonical_dangerous_ingredient_list) + ".")

class AOC_Tests(unittest.TestCase):
    def test_ex1(self):
        return self.assertEqual(solve(["mxmxvkd kfcds sqjhc nhms (contains dairy, fish)",
                                       "trh fvjkl sbzzf mxmxvkd (contains dairy)",
                                       "sqjhc fvjkl (contains soy)",
                                       "sqjhc mxmxvkd sbzzf (contains fish)"]), "mxmxvkd,sqjhc,fvjkl")

run(main)
