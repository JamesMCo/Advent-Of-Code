#!/usr/bin/env python3

#Advent of Code
#2020 Day 4, Part 2
#Solution by James C. (https://github.com/JamesMCo)

import os, sys
sys.path.append(os.path.abspath("../.."))
import unittest, util.read
from util.tests import run

import re

def solve(puzzle_input):
    birth_year  = re.compile("(19[2-9][0-9])|(200[0-2])")
    issue_year  = re.compile("(201[0-9])|(2020)")
    exp_year    = re.compile("(202[0-9])|(2030)")
    height_cm   = "((1[5-8][0-9])|(19[0-3]))cm"
    height_in   = "((59|6[0-9]|7[0-6]))in"
    height      = re.compile(f"({height_cm})|({height_in})")
    colour_hex  = re.compile("#[0-9a-f]{6}")
    colour_name = re.compile("(amb)|(blu)|(brn)|(gry)|(grn)|(hzl)|(oth)")
    pid         = re.compile("\d{9}")
    
    def make_passport(data):
        output = {}
        for entry in data.split():
            key = entry.split(":")[0]
            val = entry.split(":")[1]
            output[key] = val
        return output

    def validate_passport(passport):
        for field in ["byr", "iyr", "eyr", "hgt", "hcl", "ecl", "pid"]:
            if field not in passport.keys():
                return False

        if not re.fullmatch(birth_year, passport["byr"]):
            return False
        if not re.fullmatch(issue_year, passport["iyr"]):
            return False
        if not re.fullmatch(exp_year, passport["eyr"]):
            return False
        if not re.fullmatch(height, passport["hgt"]):
            return False
        if not re.fullmatch(colour_hex, passport["hcl"]):
            return False
        if not re.fullmatch(colour_name, passport["ecl"]):
            return False
        if not re.fullmatch(pid, passport["pid"]):
            return False

        return True

    passports = []
    working = ""
    for line in puzzle_input + [""]:
        if line != "":
            working += line + " "
        else:
            passports.append(make_passport(working))
            working = ""

    return sum(validate_passport(p) for p in passports)

def main():
    puzzle_input = util.read.as_lines()

    passports = solve(puzzle_input)

    print("The number of valid passports is " + str(passports) + ".")

class AOC_Tests(unittest.TestCase):
    def test_ex1(self):
        return self.assertEqual(solve(["eyr:1972 cid:100",
                                       "hcl:#18171d ecl:amb hgt:170 pid:186cm iyr:2018 byr:1926",
                                       "",
                                       "iyr:2019",
                                       "hcl:#602927 eyr:1967 hgt:170cm",
                                       "ecl:grn pid:012533040 byr:1946",
                                       "",
                                       "hcl:dab227 iyr:2012",
                                       "ecl:brn hgt:182cm pid:021572410 eyr:2020 byr:1992 cid:277",
                                       "",
                                       "hgt:59cm ecl:zzz",
                                       "eyr:2038 hcl:74454a iyr:2023",
                                       "pid:3556412378 byr:2007"]), 0)

    def test_ex2(self):
        return self.assertEqual(solve(["pid:087499704 hgt:74in ecl:grn iyr:2012 eyr:2030 byr:1980",
                                       "hcl:#623a2f",
                                       "",
                                       "eyr:2029 ecl:blu cid:129 byr:1989",
                                       "iyr:2014 pid:896056539 hcl:#a97842 hgt:165cm",
                                       "",
                                       "hcl:#888785",
                                       "hgt:164cm byr:2001 iyr:2015 cid:88",
                                       "pid:545766238 ecl:hzl",
                                       "eyr:2022",
                                       "",
                                       "iyr:2010 hgt:158cm hcl:#b6652a ecl:blu byr:1944 eyr:2021 pid:093154719"]), 4)

run(main)
