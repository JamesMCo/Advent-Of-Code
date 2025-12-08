#!/usr/bin/env python3

#Advent of Code
#2025 Day 8, Part 2
#Solution by James C. (https://github.com/JamesMCo)

import os, sys
sys.path.append(os.path.abspath("../.."))
import unittest, util.read
from util.tests import run

from bisect import insort
from itertools import combinations
from math import prod, sqrt

def solve(puzzle_input: list[str]) -> int:
    boxes: list[tuple[int, int, int]] = [tuple(map(int, line.split(","))) for line in puzzle_input]
    box_count: int = len(boxes)

    distances: list[tuple[float, tuple[int, int, int], tuple[int, int, int]]] = []
    for a, b in combinations(boxes, 2):
        distance = sqrt((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2 + (a[2] - b[2]) ** 2)
        insort(distances, (distance, a, b), key=lambda t: t[0])

    circuits: list[set[tuple[int, int, int]]] = []
    def connect_boxes(box_a: tuple[int, int, int], box_b: tuple[int, int, int]):
        connected_to: set[tuple[int, int, int]] | None = None
        for circuit in circuits:
            if box_a in circuit or box_b in circuit:
                if connected_to is None:
                    circuit.add(box_a)
                    circuit.add(box_b)
                    connected_to = circuit
                else:
                    # Bridging the gap between two circuits
                    # Move everything from one circuit to the other (empty circuits are cleaned up later)
                    connected_to.update(circuit)
                    circuit.clear()
        if connected_to is None:
            circuits.append({box_a, box_b})

        # Remove empty circuits
        for i in range(len(circuits) - 1, -1, -1):
            if not circuits[i]:
                circuits.pop(i)

    for _, a, b in distances:
        connect_boxes(a, b)
        if len(circuits) == 1 and len(circuits[0]) == box_count:
            return a[0] * b[0]

def main() -> tuple[str, int]:
    puzzle_input = util.read.as_lines()

    return "The product of the x coordinates of the final two boxes to be connected is {}.", solve(puzzle_input)

class AOC_Tests(unittest.TestCase):
    def test_ex1(self):
        return self.assertEqual(solve(["162,817,812",
                                       "57,618,57",
                                       "906,360,560",
                                       "592,479,940",
                                       "352,342,300",
                                       "466,668,158",
                                       "542,29,236",
                                       "431,825,988",
                                       "739,650,466",
                                       "52,470,668",
                                       "216,146,977",
                                       "819,987,18",
                                       "117,168,530",
                                       "805,96,715",
                                       "346,949,466",
                                       "970,615,88",
                                       "941,993,340",
                                       "862,61,35",
                                       "984,92,344",
                                       "425,690,689"]), 25272)

if __name__ == "__main__":
    run(main)
