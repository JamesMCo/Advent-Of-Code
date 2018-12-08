#!/usr/bin/env python3

#Advent of Code
#2016 Day 13, Part 2
#Solution by James C. (https://github.com/JamesMCo)

import os, sys
sys.path.append(os.path.abspath("../.."))
import unittest, util.read
from util.tests import run

from math import inf

def solve(puzzle_input):
    cx = 1
    cy = 1

    def getNeighbours(x, y):
        neigbours = set()
        if x != 0:
            a = x-1
            b = y
            if bin(a*a + 3*a + 2*a*b + b + b*b + puzzle_input).count("1") % 2 == 0:
                neigbours.add((a, b))
        if y != 0:
            a = x
            b = y-1
            if bin(a*a + 3*a + 2*a*b + b + b*b + puzzle_input).count("1") % 2 == 0:
                neigbours.add((a, b))
        a = x+1
        b = y
        if bin(a*a + 3*a + 2*a*b + b + b*b + puzzle_input).count("1") % 2 == 0:
            neigbours.add((a, b))
        a = x
        b = y+1
        if bin(a*a + 3*a + 2*a*b + b + b*b + puzzle_input).count("1") % 2 == 0:
            neigbours.add((a, b))

        return neigbours

    class Vertex:
        def __init__(self, x, y, dist=inf):
            self.x = x
            self.y = y
            self.dist = dist
            self.prev = None

        def __eq__(self, coords):
            return self.x == coords[0] and self.y == coords[1]

        def __hash__(self):
            return hash((self.x, self.y))

    def ModifiedDisjkstra(Graph, source):
        Q = {}
        All = {}

        for v in Graph:
            if v == source:
                Q[(v[0], v[1])] = All[(v[0], v[1])] = Vertex(v[0], v[1], 0)
            else:
                Q[(v[0], v[1])] = All[(v[0], v[1])] = Vertex(v[0], v[1])

        while Q != {}:
            u = min(Q, key=lambda x: Q[x].dist)
            Q.pop(u)

            for v in getNeighbours(u[0], u[1]):
                if v in Q:
                    alt = All[u].dist + 1
                    if alt < Q[v].dist:
                        Q[v].dist = alt
                        Q[v].prev = u

        count = 0
        for coord in All:
            if All[coord].dist <= 50:
                count += 1
        return count

    graph = set()

    for y in range(60):
        for x in range(60):
            if bin(x*x + 3*x + 2*x*y + y + y*y + puzzle_input).count("1") % 2 == 1:
                # print("#", end="")
                pass
            else:
                # print(".", end="")
                graph.add((x, y))
        # print()

    return ModifiedDisjkstra(graph, (1, 1))


def main():
    puzzle_input = util.read.as_int()

    coords = solve(puzzle_input)

    print("The number of coordinates that can be reached in 50 steps is " + str(coords) + ".")

class AOC_Tests(unittest.TestCase):
    @unittest.skip("No test cases")
    def test_ex1(self):
        pass

run(main)
