#!/usr/bin/env python3

#Advent of Code
#2019 Day 14, Part 1
#Solution by James C. (https://github.com/JamesMCo)

import os, sys
sys.path.append(os.path.abspath("../.."))
import unittest, util.read
from util.tests import run

from collections import defaultdict
import re

def solve(puzzle_input):
    reactions = {}
    chemical = re.compile(r"\d+ \w+")
    for reaction in puzzle_input:
        chemical_list = re.findall(chemical, reaction)
        
        output_quant = int(chemical_list[-1].split()[0])
        output_name  = chemical_list[-1].split()[1]
        inputs       = [{"chem": c.split()[1], "quant": int(c.split()[0])} for c in chemical_list[:-1]]
        reactions[output_name] = {"output_quant": output_quant, "inputs": inputs}

    handled = defaultdict(int)
    unhandled = defaultdict(int)
    unhandled["FUEL"] = 1

    while True:
        # Find all chemicals in the unhandled list which are not ORE, and which haven't got a surplus
        unhandled_list = [c for c in unhandled.keys() if c != "ORE" and unhandled[c] > 0]
        if len(unhandled_list) == 0:
            # Nothing without a surplus => done!
            return unhandled["ORE"]
        current_chemical = unhandled_list[0]
        current_needed   = unhandled[current_chemical]

        r = reactions[current_chemical]
        # Work out how many need to be made to get at least the target
        multiple = 1
        while r["output_quant"] * multiple < current_needed:
            multiple += 1

        # Update the lists
        unhandled[current_chemical] -= r["output_quant"] * multiple
        handled[current_chemical] += r["output_quant"] * multiple
        for c in r["inputs"]:
            unhandled[c["chem"]] += c["quant"] * multiple

def main():
    puzzle_input = util.read.as_lines()

    amount = solve(puzzle_input)

    print("The minimum amount of ORE required to produce exactly 1 FUEL is " + str(amount) + ".")

class AOC_Tests(unittest.TestCase):
    def test_ex1(self):
        self.assertEqual(solve(["10 ORE => 10 A",
                                "1 ORE => 1 B",
                                "7 A, 1 B => 1 C",
                                "7 A, 1 C => 1 D",
                                "7 A, 1 D => 1 E",
                                "7 A, 1 E => 1 FUEL"]), 31)

    def test_ex2(self):
        self.assertEqual(solve(["9 ORE => 2 A",
                                "8 ORE => 3 B",
                                "7 ORE => 5 C",
                                "3 A, 4 B => 1 AB",
                                "5 B, 7 C => 1 BC",
                                "4 C, 1 A => 1 CA",
                                "2 AB, 3 BC, 4 CA => 1 FUEL"]), 165)

    def test_ex3(self):
        self.assertEqual(solve(["157 ORE => 5 NZVS",
                                "165 ORE => 6 DCFZ",
                                "44 XJWVT, 5 KHKGT, 1 QDVJ, 29 NZVS, 9 GPVTF, 48 HKGWZ => 1 FUEL",
                                "12 HKGWZ, 1 GPVTF, 8 PSHF => 9 QDVJ",
                                "179 ORE => 7 PSHF",
                                "177 ORE => 5 HKGWZ",
                                "7 DCFZ, 7 PSHF => 2 XJWVT",
                                "165 ORE => 2 GPVTF",
                                "3 DCFZ, 7 NZVS, 5 HKGWZ, 10 PSHF => 8 KHKGT"]), 13312)

    def test_ex4(self):
        self.assertEqual(solve(["2 VPVL, 7 FWMGM, 2 CXFTF, 11 MNCFX => 1 STKFG",
                                "17 NVRVD, 3 JNWZP => 8 VPVL",
                                "53 STKFG, 6 MNCFX, 46 VJHF, 81 HVMC, 68 CXFTF, 25 GNMV => 1 FUEL",
                                "22 VJHF, 37 MNCFX => 5 FWMGM",
                                "139 ORE => 4 NVRVD",
                                "144 ORE => 7 JNWZP",
                                "5 MNCFX, 7 RFSQX, 2 FWMGM, 2 VPVL, 19 CXFTF => 3 HVMC",
                                "5 VJHF, 7 MNCFX, 9 VPVL, 37 CXFTF => 6 GNMV",
                                "145 ORE => 6 MNCFX",
                                "1 NVRVD => 8 CXFTF",
                                "1 VJHF, 6 MNCFX => 4 RFSQX",
                                "176 ORE => 6 VJHF"]), 180697)

    def test_ex5(self):
        self.assertEqual(solve(["171 ORE => 8 CNZTR",
                                "7 ZLQW, 3 BMBT, 9 XCVML, 26 XMNCP, 1 WPTQ, 2 MZWV, 1 RJRHP => 4 PLWSL",
                                "114 ORE => 4 BHXH",
                                "14 VRPVC => 6 BMBT",
                                "6 BHXH, 18 KTJDG, 12 WPTQ, 7 PLWSL, 31 FHTLT, 37 ZDVW => 1 FUEL",
                                "6 WPTQ, 2 BMBT, 8 ZLQW, 18 KTJDG, 1 XMNCP, 6 MZWV, 1 RJRHP => 6 FHTLT",
                                "15 XDBXC, 2 LTCX, 1 VRPVC => 6 ZLQW",
                                "13 WPTQ, 10 LTCX, 3 RJRHP, 14 XMNCP, 2 MZWV, 1 ZLQW => 1 ZDVW",
                                "5 BMBT => 4 WPTQ",
                                "189 ORE => 9 KTJDG",
                                "1 MZWV, 17 XDBXC, 3 XCVML => 2 XMNCP",
                                "12 VRPVC, 27 CNZTR => 2 XDBXC",
                                "15 KTJDG, 12 BHXH => 5 XCVML",
                                "3 BHXH, 2 VRPVC => 7 MZWV",
                                "121 ORE => 7 VRPVC",
                                "7 XCVML => 6 RJRHP",
                                "5 BHXH, 4 VRPVC => 5 LTCX"]), 2210736)

if __name__ == "__main__":
    run(main)
