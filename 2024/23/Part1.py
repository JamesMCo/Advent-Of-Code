#!/usr/bin/env python3

#Advent of Code
#2024 Day 23, Part 1
#Solution by James C. (https://github.com/JamesMCo)

import os, sys
sys.path.append(os.path.abspath("../.."))
import unittest, util.read
from util.tests import run

from collections import defaultdict
from itertools import combinations

def solve(puzzle_input: list[str]) -> int:
    computers: defaultdict[str, set[str]] = defaultdict(set)
    for connection in puzzle_input:
        a, b = connection.split("-")
        computers[a].add(b)
        computers[b].add(a)

    considered_sets: set[str] = set()
    found_sets: set[str] = set()

    for initial in computers:
        if len(computers[initial]) >= 2:
            for connected in combinations(computers[initial], 2):
                computer_set: set[str] = {initial}.union(connected)
                if str(sorted(computer_set)) in considered_sets:
                    continue
                considered_sets.add(str(sorted(computer_set)))
                if not any(computer[0] == "t" for computer in computer_set):
                    continue

                valid: bool = True

                for root in computer_set:
                    for other in computer_set:
                        if root == other:
                            continue
                        elif other not in computers[root] or root not in computers[other]:
                            valid = False
                            break
                    if not valid:
                        break

                if valid:
                    found_sets.add(str(sorted(computer_set)))


    return len(found_sets)

def main() -> tuple[str, int]:
    puzzle_input = util.read.as_lines()

    return "The number of sets of three inter-connected computers where at least one computer name starts with t is {}.", solve(puzzle_input)

class AOC_Tests(unittest.TestCase):
    def test_ex1(self):
        return self.assertEqual(solve(["kh-tc",
                                       "qp-kh",
                                       "de-cg",
                                       "ka-co",
                                       "yn-aq",
                                       "qp-ub",
                                       "cg-tb",
                                       "vc-aq",
                                       "tb-ka",
                                       "wh-tc",
                                       "yn-cg",
                                       "kh-ub",
                                       "ta-co",
                                       "de-co",
                                       "tc-td",
                                       "tb-wq",
                                       "wh-td",
                                       "ta-ka",
                                       "td-qp",
                                       "aq-cg",
                                       "wq-ub",
                                       "ub-vc",
                                       "de-ta",
                                       "wq-aq",
                                       "wq-vc",
                                       "wh-yn",
                                       "ka-de",
                                       "kh-ta",
                                       "co-tc",
                                       "wh-qp",
                                       "tb-vc",
                                       "td-yn"]), 7)

if __name__ == "__main__":
    run(main)
