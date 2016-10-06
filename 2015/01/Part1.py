#!/usr/bin/env python3

#Advent of Code
#Day 1, Part 1
#Solution by Jammy4312 (https://jammy4312.me)

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