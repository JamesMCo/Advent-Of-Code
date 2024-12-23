#!/usr/bin/env python3

#Advent of Code
#2024 Day 23, Part 2
#Solution by James C. (https://github.com/JamesMCo)

import os, sys
sys.path.append(os.path.abspath("../.."))
import unittest, util.read
from util.tests import run

from collections import defaultdict
from itertools import combinations

def solve(puzzle_input: list[str]) -> str:
    computers: defaultdict[str, set[str]] = defaultdict(set)
    for connection in puzzle_input:
        a, b = connection.split("-")
        computers[a].add(b)
        computers[b].add(a)

    considered_sets: set[str] = set()
    found_sets: dict[str, int] = {}
    max_connections: int = max(map(len, computers.values()))

    for initial in computers:
        for other_amount in range(1, max_connections + 1):
            for connected in combinations(computers[initial], other_amount):
                computer_set: set[str] = {initial}.union(connected)
                if (computer_set_name := ",".join(sorted(computer_set))) in considered_sets:
                    continue
                considered_sets.add(computer_set_name)
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
                    found_sets[computer_set_name] = len(computer_set)

    largest_set: int = max(found_sets.values())

    return [password for password, length in found_sets.items() if length == largest_set][0]

def main() -> tuple[str, str]:
    puzzle_input = util.read.as_lines()

    return "The password to get into the LAN party is {}.", solve(puzzle_input)

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
                                       "td-yn"]), "co,de,ka,ta")

run(main)
