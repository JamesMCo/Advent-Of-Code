#!/usr/bin/env python3

#Advent of Code
#2015 Day 17, Part 2
#Solution by James C. (https://github.com/JamesMCo)

from itertools import combinations

f = open("puzzle_input.txt")
puzzle_input = f.read().strip().split("\n")
f.close()

containers = [int(x) for x in puzzle_input]
seen = 0
minimum = len(containers)+1

for i in range(1, len(containers)+1):
    for arr in combinations(containers, i):
        if sum(arr) == 150:
            if len(arr) == minimum:
                seen += 1
            elif len(arr) < minimum:
                minimum = len(arr)
                seen = 1

print("There are " + str(seen) + " different ways to fill the minimum number of containers that can fit 150 litres of eggnog.")