#!/usr/bin/env python3

#Advent of Code
#2018 Day 18, Part 2
#Solution by James C. (https://github.com/JamesMCo)

import os, sys
sys.path.append(os.path.abspath("../.."))
import unittest, util.read
from util.tests import run

def solve(puzzle_input):
    prev_area = puzzle_input[:]
    area = []
    seen = ["".join(puzzle_input)]
    for minute in range(1_000_000_000):
        area = []
        for y, row in enumerate(prev_area):
            area.append("")
            for x, col in enumerate(row):
                neighbours = [prev_area[y_offset][x_offset]
                              for x_offset in range(x-1,x+2)
                              for y_offset in range(y-1,y+2)
                              if  (x_offset, y_offset) != (x, y)
                              and 0 <= x_offset < len(prev_area[0])
                              and 0 <= y_offset < len(prev_area)]
                if col == "." and neighbours.count("|") >= 3:
                    area[-1] += "|"
                elif col == "|" and neighbours.count("#") >= 3:
                    area[-1] += "#"
                elif col == "#" and (neighbours.count("#") == 0 or neighbours.count("|") == 0):
                    area[-1] += "."
                else:
                    area[-1] += col
        prev_area = area[:]

        temp = "".join(area)
        if temp in seen:
            minute += 1

            seen = seen[seen.index(temp):]
            target = ((1_000_000_000 - minute) % len(seen))

            temp = seen[target]
            break
        else:
            seen.append(temp)

    return temp.count("|") * temp.count("#")

def main():
    puzzle_input = util.read.as_lines()

    resource_value = solve(puzzle_input)

    print("The total resource value of the collection area after 1,000,000,000 minutes is " + str(resource_value) + ".")

class AOC_Tests(unittest.TestCase):
    @unittest.skip("No test cases")
    def test_ex1(self):
        pass

if __name__ == "__main__":
    run(main)
