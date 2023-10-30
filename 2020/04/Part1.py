#!/usr/bin/env python3

#Advent of Code
#2020 Day 4, Part 1
#Solution by James C. (https://github.com/JamesMCo)

import os, sys
sys.path.append(os.path.abspath("../.."))
import unittest, util.read
from util.tests import run

import re

def solve(puzzle_input):
    passport_data = re.compile(r"(\w+):(\S+)")

    def consume_passport():
        output = []
        while puzzle_input:
            line = puzzle_input.pop(0)
            if line == "":
                break
            output.append(line)
        return " ".join(output)

    def make_passport(data):
        return {key:val for (key, val) in re.findall(passport_data, data)}

    def validate_passport(passport):
        for field in ["byr", "iyr", "eyr", "hgt", "hcl", "ecl", "pid"]:
            if field not in passport.keys():
                return False
        return True

    passports = []
    while puzzle_input:
        passports.append(make_passport(consume_passport()))

    return sum(validate_passport(p) for p in passports)

def main():
    puzzle_input = util.read.as_lines()

    passports = solve(puzzle_input)

    print("The number of valid passports is " + str(passports) + ".")

class AOC_Tests(unittest.TestCase):
    def test_ex1(self):
        return self.assertEqual(solve(["ecl:gry pid:860033327 eyr:2020 hcl:#fffffd",
                                       "byr:1937 iyr:2017 cid:147 hgt:183cm",
                                       "",
                                       "iyr:2013 ecl:amb cid:350 eyr:2023 pid:028048884",
                                       "hcl:#cfa07d byr:1929",
                                       "",
                                       "hcl:#ae17e1 iyr:2013",
                                       "eyr:2024",
                                       "ecl:brn pid:760753108 byr:1931",
                                       "hgt:179cm",
                                       "",
                                       "hcl:#cfa07d eyr:2025 pid:166559648",
                                       "iyr:2011 ecl:brn hgt:59in"]), 2)

run(main)
