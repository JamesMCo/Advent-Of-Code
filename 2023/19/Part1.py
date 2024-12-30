#!/usr/bin/env python3

#Advent of Code
#2023 Day 19, Part 1
#Solution by James C. (https://github.com/JamesMCo)

import os, sys
sys.path.append(os.path.abspath("../.."))
import unittest, util.read
from util.tests import run

import re
import typing as t

def solve(puzzle_input: list[str]) -> int:
    class Part:
        x: int
        m: int
        a: int
        s: int

        ratings_pattern: re.Pattern = re.compile(r"\{x=(\d+),m=(\d+),a=(\d+),s=(\d+)}")

        def __init__(self: t.Self, ratings: str) -> None:
            self.x, self.m, self.a, self.s = map(int, self.ratings_pattern.match(ratings).groups())

        def __str__(self: t.Self) -> str:
            return f"{{x={self.x},m={self.m},a={self.a},s={self.s}}}"

    class Workflow:
        name: str
        rules: list[str]

        rule_pattern: re.Pattern = re.compile(r"([xmas])([<>])(\d+):(\w+)")

        def __init__(self: t.Self, workflow_description: str) -> None:
            self.name = workflow_description.split("{")[0]
            self.rules = workflow_description.split("{")[1][:-1].split(",")

        def handle(self: t.Self, part: Part) -> str:
            for rule in self.rules:
                if ":" in rule:
                    category, comparison, value, result = self.rule_pattern.match(rule).groups()
                    if (comparison == "<" and part.__getattribute__(category) < int(value))\
                    or (comparison == ">" and part.__getattribute__(category) > int(value)):
                        return result
                else:
                    return rule

    def parse_input(lines: list[str]) -> tuple[dict[str, Workflow], list[Part]]:
        output_workflows = {}
        output_parts = []

        i = 0
        while lines[i] != "":
            new_workflow = Workflow(lines[i])
            output_workflows[new_workflow.name] = new_workflow
            i += 1

        i += 1
        while i < len(lines):
            output_parts.append(Part(lines[i]))
            i += 1

        return output_workflows, output_parts

    workflows, parts = parse_input(puzzle_input)

    def handle_part(part: Part) -> int:
        current_workflow = "in"
        while True:
            match workflows[current_workflow].handle(part):
                case "A":  return part.x + part.m + part.a + part.s
                case "R":  return 0
                case name: current_workflow = name

    return sum(map(handle_part, parts))

def main() -> tuple[str, int]:
    puzzle_input = util.read.as_lines()

    return "The sum of all the rating numbers for all accepted parts is {}.", solve(puzzle_input)

class AOC_Tests(unittest.TestCase):
    def test_ex1(self):
        return self.assertEqual(solve(["px{a<2006:qkq,m>2090:A,rfg}",
                                       "pv{a>1716:R,A}",
                                       "lnx{m>1548:A,A}",
                                       "rfg{s<537:gd,x>2440:R,A}",
                                       "qs{s>3448:A,lnx}",
                                       "qkq{x<1416:A,crn}",
                                       "crn{x>2662:A,R}",
                                       "in{s<1351:px,qqz}",
                                       "qqz{s>2770:qs,m<1801:hdj,R}",
                                       "gd{a>3333:R,R}",
                                       "hdj{m>838:A,pv}",
                                       "",
                                       "{x=787,m=2655,a=1222,s=2876}",
                                       "{x=1679,m=44,a=2067,s=496}",
                                       "{x=2036,m=264,a=79,s=2244}",
                                       "{x=2461,m=1339,a=466,s=291}",
                                       "{x=2127,m=1623,a=2188,s=1013}"]), 19114)

if __name__ == "__main__":
    run(main)
