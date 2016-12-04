#!/usr/bin/env python3

#Advent of Code
#Day 4, Part 1
#Solution by Jammy4312 (https://jammy4312.me)

f = open("puzzle_input.txt")
puzzle_input = f.read().split("\n")
f.close()

from collections import Counter

sector_ids = 0

def getchecksum(s):
    c = Counter(s)
    d = {}
    for l in c:
        if c[l] in d:
            d[c[l]] += l
        else:
            d[c[l]] = l
    f = ""
    for i in sorted(d, reverse=True):
        f += "".join(sorted(list(d[i])))
    return f[:5]

for room in puzzle_input:
    if room == "": continue
    working = "".join(sorted(room.split("-")[:-1]))
    if getchecksum(working) == room.split("[")[1][:-1]:
        sector_ids += int(room.split("-")[-1][:3])

print("The sum of the sector IDs is " + str(sector_ids) + ".")
