#!/usr/bin/env python3

#Advent of Code
#2023 Day 19, Part 2
#Solution by James C. (https://github.com/JamesMCo)

import os, sys
sys.path.append(os.path.abspath("../.."))
import unittest, util.read
from util.tests import run

import re
import typing as t

def solve(puzzle_input: list[str]) -> int:
    class Workflow:
        name: str
        rules: list[str]

        rule_pattern: re.Pattern = re.compile(r"([xmas])([<>])(\d+):(\w+)")

        def __init__(self: t.Self, workflow_description: str) -> None:
            self.name = workflow_description.split("{")[0]
            self.rules = workflow_description.split("{")[1][:-1].split(",")

    def parse_input(lines: list[str]) -> dict[str, Workflow]:
        output_workflows = {}

        i = 0
        while lines[i] != "":
            new_workflow = Workflow(lines[i])
            output_workflows[new_workflow.name] = new_workflow
            i += 1

        return output_workflows

    workflows = parse_input(puzzle_input)

    def split_range(lower: int, upper: int, comparison: str, threshold: int) -> tuple[t.Optional[tuple[int, int]], t.Optional[tuple[int, int]]]:
        # First element of returned tuple is the true range
        # Second element of returned tuple is the false range
        #
        # There are more clever ways of calculating this, but
        # I kept running into edge cases and errors. Might
        # fix it up at a later time, but it still runs in
        # a fraction of a second, so not too bad!

        true_lower, true_upper = None, None
        false_lower, false_upper = None, None
        for i in range(lower, upper):
            if (comparison == "<" and i < threshold) or (comparison == ">" and i > threshold):
                true_lower = true_lower or i
                true_upper = i
            else:
                false_lower = false_lower or i
                false_upper = i
        if true_lower and false_lower:
            return (true_lower, true_upper + 1), (false_lower, false_upper + 1)
        elif true_lower:
            return (true_lower, true_upper + 1), None
        else:
            return None, (false_lower, false_upper + 1)

    def find_accepted_parts(workflow: str = "in",
                            x: tuple[int, int] = (1, 4001),
                            m: tuple[int, int] = (1, 4001),
                            a: tuple[int, int] = (1, 4001),
                            s: tuple[int, int] = (1, 4001)) -> int:
        total = 0

        for rule in workflows[workflow].rules:
            if ":" in rule:
                category, comparison, value, result = Workflow.rule_pattern.match(rule).groups()
                range_being_tested: tuple[int, int]
                match category:
                    case "x": range_being_tested = x
                    case "m": range_being_tested = m
                    case "a": range_being_tested = a
                    case "s": range_being_tested = s

                true_range, false_range = split_range(*range_being_tested, comparison, int(value))
                if true_range:
                    match result:
                        case "A":
                            total += (x[1] - x[0] if category != "x" else true_range[1] - true_range[0]) *\
                                     (m[1] - m[0] if category != "m" else true_range[1] - true_range[0]) *\
                                     (a[1] - a[0] if category != "a" else true_range[1] - true_range[0]) *\
                                     (s[1] - s[0] if category != "s" else true_range[1] - true_range[0])
                        case "R":
                            pass
                        case _:
                            total += find_accepted_parts(result,
                                                         true_range if category == "x" else x,
                                                         true_range if category == "m" else m,
                                                         true_range if category == "a" else a,
                                                         true_range if category == "s" else s)

                if false_range:
                    match category:
                        case "x": x = false_range
                        case "m": m = false_range
                        case "a": a = false_range
                        case "s": s = false_range
                else:
                    break
            else:
                match rule:
                    case "A":
                        total += (x[1] - x[0]) * (m[1] - m[0]) * (a[1] - a[0]) * (s[1] - s[0])
                    case "R":
                        pass
                    case _:
                        total += find_accepted_parts(rule, x, m, a, s)
        return total

    return find_accepted_parts()

def main() -> tuple[str, int]:
    puzzle_input = util.read.as_lines()

    return "The number of distinct combinations of ratings that will be accepted is {}.", solve(puzzle_input)

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
                                       "{x=2127,m=1623,a=2188,s=1013}"]), 167409079868000)

run(main)
