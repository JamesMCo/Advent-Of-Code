#!/usr/bin/env python3

#Advent of Code
#Day 13, Part 2
#Solution by James C. (https://github.com/JamesMCo)

from itertools import permutations

f = open("puzzle_input.txt")
puzzle_input = f.read().strip().split("\n")
f.close()

people = []
units = {}
for line in puzzle_input:
    line = line.split()
    for person in [line[0], line[-1][:-1]]:
        if person not in people:
            people.append(person)
    if line[2] == "gain":
        units[f"{line[0]},{line[-1][:-1]}"] = int(line[3])
    else:
        units[f"{line[0]},{line[-1][:-1]}"] = -int(line[3])
for person in people:
    units[f"{person},You"] = 0
    units[f"You,{person}"] = 0
people.append("You")

def sat(a, b):
    return units[f"{a},{b}"] + units[f"{b},{a}"]

highest = 0
for arr in permutations(people):
    running = 0
    temp = list(arr[1:])
    temp.append(arr[0])
    for a, b in zip(arr, temp):
        running += sat(a, b)
    if running > highest:
        highest = running

print("The optimal seating arrangement has a total change in happiness of " + str(highest) + ".")