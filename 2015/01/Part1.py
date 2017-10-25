#!/usr/bin/env python3

#Advent of Code
#Day 1, Part 1
#Solution by James C. (https://github.com/JamesMCo)

f = open("puzzle_input.txt")
puzzle_input = f.read()
f.close()

floor = 0

for i in puzzle_input:
    if i == "(":
        floor += 1
    else:
        floor -= 1

print("Santa's instructions take him to Floor " + str(floor) + ".")
