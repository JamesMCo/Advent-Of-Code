#!/usr/bin/env python3

#Advent of Code
#2020 Day 19, Part 1
#Solution by James C. (https://github.com/JamesMCo)

import os, sys
sys.path.append(os.path.abspath("../.."))
import unittest, util.read
from util.tests import run

from functools import cache
import re

def solve(puzzle_input):
    rule_char = re.compile(r"(\d+): \"(\w+)\"")
    rules     = {}

    def consume_section():
        output = []
        while puzzle_input:
            line = puzzle_input.pop(0)
            if line == "":
                break
            output.append(line)
        return output

    @cache
    def rule_to_regex(i):
        if type(i) == str:
            return i
        elif type(rules[i][0]) == list:
            return f"({'|'.join(''.join(rule_to_regex(j) for j in subrule_list) for subrule_list in rules[i])})"
        else:
            return f"({''.join(rule_to_regex(j) for j in rules[i])})"

    for line in consume_section():
        if (r := re.fullmatch(rule_char, line)):
            rules[int(r.group(1))] = r.group(2)
        else:
            num = int(line.split(":")[0])
            if "|" in line:
                left  = re.findall(r"\d+", line.split(":")[1].split("|")[0])
                right = re.findall(r"\d+", line.split("|")[1])
                rules[num] = [[int(x) for x in left], [int(x) for x in right]]
            else:
                rules[num] = [int(x) for x in re.findall(r"\d+", line.split(":")[1])]

    rule_0 = re.compile(rule_to_regex(0))

    return sum(re.fullmatch(rule_0, line) != None for line in consume_section())

def main():
    puzzle_input = util.read.as_lines()

    messages = solve(puzzle_input)

    print("The number of valid messages is " + str(messages) + ".")

class AOC_Tests(unittest.TestCase):
    def test_ex1(self):
        return self.assertEqual(solve(["0: 4 1 5",
                                       "1: 2 3 | 3 2",
                                       "2: 4 4 | 5 5",
                                       "3: 4 5 | 5 4",
                                       "4: \"a\"",
                                       "5: \"b\"",
                                       "",
                                       "ababbb",
                                       "bababa",
                                       "abbbab",
                                       "aaabbb",
                                       "aaaabbb"]), 2)

if __name__ == "__main__":
    run(main)
