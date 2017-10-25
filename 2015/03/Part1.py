#!/usr/bin/env python3

#Advent of Code
#Day 3, Part 1
#Solution by James C. (https://github.com/JamesMCo)

f = open("puzzle_input.txt")
puzzle_input = f.read()
f.close()

current = [0, 0]
houses = set("00")

for i in puzzle_input:
    if   i == "^":
        current[1] += 1
    elif i == ">":
        current[0] += 1
    elif i == "v":
        current[1] -= 1
    else:
        current[0] -= 1

    houses.add(str(current[0])+str(current[1]))

print("Santa will visit " + str(len(houses)) + " houses.")
