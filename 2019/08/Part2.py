#!/usr/bin/env python3

#Advent of Code
#2019 Day 8, Part 2
#Solution by James C. (https://github.com/JamesMCo)

import os, sys
sys.path.append(os.path.abspath("../.."))
import unittest, util.read
from util.tests import run

def solve(puzzle_input, width=25, height=6):
    def data_to_layers(data, width, height):
        layers = []
        while len(data) > 0:
            l, data = data[:width*height], data[width*height:]
            layers.append(l)
        return layers

    def combine_layers(vals):
        for v in vals:
            if v != "2":
                return v
        return "2"

    layers = data_to_layers(puzzle_input, width, height)
    
    image_data = []
    for i in range(len(layers[0])):
        image_data.append(combine_layers(x[i] for x in layers))
    
    return "".join(image_data)

def main():
    puzzle_input = util.read.as_string()

    image = solve(puzzle_input)

    print("The image is:")
    while len(image) > 0:
        l, image = image[:25], image[25:]
        print(l.replace("0", " ").replace("1", "*"))

class AOC_Tests(unittest.TestCase):
    def test_ex1(self):
        self.assertEqual(solve("0222112222120000", 2, 2), "0110")

if __name__ == "__main__":
    run(main)
