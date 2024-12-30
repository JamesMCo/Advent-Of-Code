#!/usr/bin/env python3

#Advent of Code
#2020 Day 23, Part 2
#Solution by James C. (https://github.com/JamesMCo)

import os, sys
sys.path.append(os.path.abspath("../.."))
import unittest, util.read
from util.tests import run

def solve(puzzle_input, moves=10_000_000):
    class Node:
        def __init__(self, value):
            self.value = value
            self.next = None
            self.prev = None

    def link(prev_node, next_node):
        prev_node.next = next_node
        next_node.prev = prev_node

    class CupsGame:
        def __init__(self, initial_order):
            initial_order = [int(x) for x in initial_order]
            self.min = min(initial_order)
            self.max = 1_000_000
            self.current_cup = initial_order[0]

            self.cups = [None for x in range(1_000_002)]
            last_created  = None
            first_created = None
            for cup in [int(x) for x in initial_order] + [x for x in range(max(initial_order)+1, 1_000_001)]:
                new = Node(cup)
                self.cups[cup] = new
                if first_created == None: first_created = new
                if last_created != None: link(last_created, new)
                last_created = new
            link(last_created, first_created)

        def play(self, moves):
            for move in range(moves):
                self.turn()

        def turn(self):
            removed_cups = self.cups[self.current_cup].next
            link(self.cups[self.current_cup], self.cups[self.current_cup].next.next.next.next)

            destination = self.find_next_destination(self.current_cup, [removed_cups.value, removed_cups.next.value, removed_cups.next.next.value])
            destination_node = self.cups[destination]

            link(removed_cups.next.next, destination_node.next)
            link(destination_node, removed_cups)

            self.current_cup = self.cups[self.current_cup].next.value

        def find_next_destination(self, current_cup, removed_cups):
            candidate = current_cup - 1
            while True:
                if candidate < self.min:
                    candidate = self.max

                if candidate not in removed_cups:
                    return candidate

                candidate -= 1

        def label_product(self):
            return self.cups[1].next.value * self.cups[1].next.next.value

    game = CupsGame(puzzle_input)
    game.play(moves)
    return game.label_product()

def main():
    puzzle_input = util.read.as_string()

    labels = solve(puzzle_input)

    print("The product of the labels is " + str(labels) + ".")

class AOC_Tests(unittest.TestCase):
    def test_ex1(self):
        return self.assertEqual(solve("389125467"), 149245887792)

if __name__ == "__main__":
    run(main)
