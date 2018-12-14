#!/usr/bin/env python3

#Advent of Code
#2018 Day 13, Part 2
#Solution by James C. (https://github.com/JamesMCo)

import os, sys
sys.path.append(os.path.abspath("../.."))
import unittest, util.read
from util.tests import run

def solve(puzzle_input):
    tracks = []
    carts  = []
    class Cart:
        forward_slash  = {"^": ">",
                          "v": "<",
                          "<": "v",
                          ">": "^"}
        backward_slash = {"^": "<",
                          "v": ">",
                          "<": "^",
                          ">": "v"}
        turn_left      = {"^": "<",
                          "v": ">",
                          "<": "v",
                          ">": "^"}
        turn_right     = {"^": ">",
                          "v": "<",
                          "<": "^",
                          ">": "v"}

        def __init__(self, x, y, direction):
            self.x = x
            self.y = y
            self.direction = direction
            self.next_turn = "left"
            self.cartID = len(carts)

            self.active = 1

        def __lt__(self, other):
            if self.y < other.y:
                return True
            elif self.y > other.y:
                return False
            else:
                if self.x < other.x:
                    return True
                else:
                    return False

        def step(self):
            if self.active == 0:
                return

            if self.direction == "^":
                self.y -= 1
            elif self.direction == "v":
                self.y += 1
            elif self.direction == "<":
                self.x -= 1
            else:
                self.x += 1

            if tracks[self.y][self.x] == "/":
                self.direction = Cart.forward_slash[self.direction]
            elif tracks[self.y][self.x] == "\\":
                self.direction = Cart.backward_slash[self.direction]
            elif tracks[self.y][self.x] == "+":
                if self.next_turn == "left":
                    self.direction = Cart.turn_left[self.direction]
                    self.next_turn = "straight"
                elif self.next_turn == "straight":
                    self.next_turn = "right"
                elif self.next_turn == "right":
                    self.direction = Cart.turn_right[self.direction]
                    self.next_turn = "left"

            for cart in carts:
                if cart.cartID != self.cartID and cart.active == 1 and cart.x == self.x and cart.y == self.y:
                    self.active = 0
                    cart.active = 0

    for y, line in enumerate(puzzle_input):
        tracks.append("")
        for x, c in enumerate(line):
            if c in "v^":
                carts.append(Cart(x, y, c))
                tracks[-1] += "|"
            elif c in "<>":
                carts.append(Cart(x, y, c))
                tracks[-1] += "-"
            else:
                tracks[-1] += c

    while True:
        carts.sort()
        for cart in carts:
            cart.step()
        if sum(c.active for c in carts) == 1:
            for cart in carts:
                if cart.active == 1:
                    return f"{cart.x},{cart.y}"

def main():
    puzzle_input = util.read.as_lines_sans_ending_line()

    coord = solve(puzzle_input)

    print("The location of final remaining cart is " + str(coord) + ".")

class AOC_Tests(unittest.TestCase):
    def test_ex1(self):
        self.assertEqual(solve(["/>-<\\  ",
                                "|   |  ",
                                "| /<+-\\",
                                "| | | v",
                                "\\>+</ |",
                                "  |   ^",
                                "  \\<->/"]), "6,4")

run(main)
