#!/usr/bin/env python3

#Advent of Code
#Day 9, Part 2
#Solution by James C. (https://github.com/JamesMCo)

from itertools import permutations

f = open("puzzle_input.txt")
puzzle_input = f.read().strip().split("\n")
f.close()

places = []
distances = {}

for line in puzzle_input:
    line = line.strip().split()
    for place in [line[0], line[2]]:
        if place not in places:
            places.append(place)
    distances[str(sorted([line[0], line[2]]))] = int(line[4])

highest = 0
for route in permutations(places):
    running = 0
    for a, b in zip(route[:-1], route[1:]):
        running += distances[str(sorted([a, b]))]
    if running > highest:
        highest = running

print("The distance of the longest route is " + str(highest) + ".")