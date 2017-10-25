#!/usr/bin/env python3

#Advent of Code
#Day 3, Part 1
#Solution by James C. (https://github.com/JamesMCo)

f = open("puzzle_input.txt")
puzzle_input = f.read().split("\n")
f.close()

possible = 0

for t in puzzle_input:
    if t == "": continue
    values = t.split(" ")
    sides = []
    for v in values:
        if v != "":
            sides.append(v)
    if (int(sides[0]) + int(sides[1]) > int(sides[2]) and
        int(sides[1]) + int(sides[2]) > int(sides[0]) and
        int(sides[2]) + int(sides[0]) > int(sides[1])):
        possible += 1

print("There are " + str(possible) + " possible triangles.")
