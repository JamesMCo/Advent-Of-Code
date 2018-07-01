#!/usr/bin/env python3

#Advent of Code
#Day 17, Part 1
#Solution by James C. (https://github.com/JamesMCo)

from itertools import combinations

f = open("puzzle_input.txt")
puzzle_input = f.read().strip().split("\n")
f.close()

containers = [int(x) for x in puzzle_input]
seen = 0

for i in range(1, len(containers)+1):
    for arr in combinations(containers, i):
        if sum(arr) == 150:
            seen += 1

print("There are " + str(seen) + " combinations of containers that fit 150 litres of eggnog.")