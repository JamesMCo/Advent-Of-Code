#!/usr/bin/env python3

#Advent of Code
#Day 2, Part 2
#Solution by Jammy4312 (https://jammy4312.me)

f = open("puzzle_input.txt")
puzzle_input = f.read()
f.close()

current = [[0, 0], [0, 0]]
houses = set()
santa = 0

for i in puzzle_input:
    if   i == "^":
        current[santa][1] += 1
    elif i == ">":
        current[santa][0] += 1
    elif i == "v":
        current[santa][1] -= 1
    else:
        current[santa][0] -= 1

    houses.add(str(current[santa][0])+str(current[santa][1]))

    if santa == 0:
        santa = 1
    else:
        santa = 0

print("Santa and Robo-Santa will visit " + str(len(houses)) + " houses.")
