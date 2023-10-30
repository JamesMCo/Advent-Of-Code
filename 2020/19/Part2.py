#!/usr/bin/env python3

#Advent of Code
#2020 Day 19, Part 2
#Solution by James C. (https://github.com/JamesMCo)

import os, sys
sys.path.append(os.path.abspath("../.."))
import unittest, util.read
from util.tests import run

import regex
# Notably, not "re" - the regex module supports recursive regular expressions

def solve(puzzle_input):
    rule_char = regex.compile(r"(\d+): \"(\w+)\"")
    rules     = {}

    def consume_section():
        output = []
        while puzzle_input:
            line = puzzle_input.pop(0)
            if line == "":
                break
            output.append(line)
        return output

    class RegexBuilder:
        def __init__(self):
            self.inserted11 = False
            # Use a variable to track whether the capture group releven
            # has been added to the regex yet. It should only be added
            # once, so don't add it if self.inserted11 is already True.

        def rule_to_regex(self, i):
            if i == 8:
                return f"(({self.rule_to_regex(42)})+)"
            elif i == 11:
                if self.inserted11:
                    return f"(?P=releven)"
                else:
                    self.inserted11 = True
                    return f"(?P<releven>(({self.rule_to_regex(42)}(?&releven)?{self.rule_to_regex(31)})))"
                # Recursive regex solution concieved after reading through the subreddit
                # and some online research (this tutorial was particularly helpful:
                # https://www.rexegg.com/regex-recursion.html )
            elif type(i) == str:
                return i
            elif type(rules[i][0]) == list:
                return f"({'|'.join(''.join(self.rule_to_regex(j) for j in subrule_list) for subrule_list in rules[i])})"
            else:
                return f"({''.join(self.rule_to_regex(j) for j in rules[i])})"

        def build(self):
            return self.rule_to_regex(0)

    # Rules 8 and 11 are entered into the rules dictionary,
    # but rule_to_regex(8) and rule_to_regex(11) are hardcoded rather than calculated
    for line in consume_section() + ["8: 42 | 42 8", "11: 42 31 | 42 11 31"]:
        if (r := regex.fullmatch(rule_char, line)):
            rules[int(r.group(1))] = r.group(2)
        else:
            num = int(line.split(":")[0])
            if "|" in line:
                left  = regex.findall(r"\d+", line.split(":")[1].split("|")[0])
                right = regex.findall(r"\d+", line.split("|")[1])
                rules[num] = [[int(x) for x in left], [int(x) for x in right]]
            else:
                rules[num] = [int(x) for x in regex.findall(r"\d+", line.split(":")[1])]

    rule_0 = regex.compile(RegexBuilder().build())

    return sum(regex.fullmatch(rule_0, line) != None for line in consume_section())

def main():
    puzzle_input = util.read.as_lines()

    messages = solve(puzzle_input)

    print("The number of valid messages is " + str(messages) + ".")

class AOC_Tests(unittest.TestCase):
    def test_ex1(self):
        return self.assertEqual(solve(["42: 9 14 | 10 1",
                                       "9: 14 27 | 1 26",
                                       "10: 23 14 | 28 1",
                                       "1: \"a\"",
                                       "11: 42 31",
                                       "5: 1 14 | 15 1",
                                       "19: 14 1 | 14 14",
                                       "12: 24 14 | 19 1",
                                       "16: 15 1 | 14 14",
                                       "31: 14 17 | 1 13",
                                       "6: 14 14 | 1 14",
                                       "2: 1 24 | 14 4",
                                       "0: 8 11",
                                       "13: 14 3 | 1 12",
                                       "15: 1 | 14",
                                       "17: 14 2 | 1 7",
                                       "23: 25 1 | 22 14",
                                       "28: 16 1",
                                       "4: 1 1",
                                       "20: 14 14 | 1 15",
                                       "3: 5 14 | 16 1",
                                       "27: 1 6 | 14 18",
                                       "14: \"b\"",
                                       "21: 14 1 | 1 14",
                                       "25: 1 1 | 1 14",
                                       "22: 14 14",
                                       "8: 42",
                                       "26: 14 22 | 1 20",
                                       "18: 15 15",
                                       "7: 14 5 | 1 21",
                                       "24: 14 1",
                                       "",
                                       "abbbbbabbbaaaababbaabbbbabababbbabbbbbbabaaaa",
                                       "bbabbbbaabaabba",
                                       "babbbbaabbbbbabbbbbbaabaaabaaa",
                                       "aaabbbbbbaaaabaababaabababbabaaabbababababaaa",
                                       "bbbbbbbaaaabbbbaaabbabaaa",
                                       "bbbababbbbaaaaaaaabbababaaababaabab",
                                       "ababaaaaaabaaab",
                                       "ababaaaaabbbaba",
                                       "baabbaaaabbaaaababbaababb",
                                       "abbbbabbbbaaaababbbbbbaaaababb",
                                       "aaaaabbaabaaaaababaa",
                                       "aaaabbaaaabbaaa",
                                       "aaaabbaabbaaaaaaabbbabbbaaabbaabaaa",
                                       "babaaabbbaaabaababbaabababaaab",
                                       "aabbbbbaabbbaaaaaabbbbbababaaaaabbaaabba"]), 12)

run(main)
