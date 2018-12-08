#!/usr/bin/env python3

#Advent of Code
#2015 Day 16, Part 2
#Solution by James C. (https://github.com/JamesMCo)

f = open("puzzle_input.txt")
puzzle_input = f.read().split("\n")[:-1]
f.close()

data = {
    "children": 3,
    "cats": 7,
    "samoyeds": 2,
    "pomeranians": 3,
    "akitas": 0,
    "vizslas": 0,
    "goldfish": 5,
    "trees": 3,
    "cars": 2,
    "perfumes": 1
}

sues = []
for sue in puzzle_input:
    d = {}
    for i in range(2, len(sue.split()), 2):
        if sue.split()[i+1][-1] == ",":
            d[sue.split()[i][:-1]] = int(sue.split()[i+1][:-1])
        else:
            d[sue.split()[i][:-1]] = int(sue.split()[i+1])
    sues.append(d)

for i, sue in enumerate(sues):
    found = True
    for d in sue:
        if d in ["cats", "trees"] and data[d] >= sue[d]:
            found = False
            break
        elif d in ["pomeranians", "goldfish"] and data[d] <= sue[d]:
            found = False
            break
        if d not in ["cats", "trees", "pomeranians", "goldfish"] and sue[d] != data[d]:
            found = False
            break
    if found:
        print("The number of the Sue that got the gift is " + str(i+1) + ".")
        # break