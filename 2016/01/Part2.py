#!/usr/bin/env python3

#Advent of Code
#Day 1, Part 2
#Solution by James C. (https://github.com/JamesMCo)

f = open("puzzle_input.txt")
puzzle_input = f.read().split(", ")
f.close()

from math import fabs

origin = (0, 0)
here   = [0, 0]
visit  = []
facing = 0 #N=1, E=1, S=2, W=3

for i in puzzle_input:
    if i[0] == "L":
        facing -= 1
        if facing == -1: facing = 3
    else:
        facing += 1
        if facing == 4: facing = 0
    moves = int(i[1:])
    while moves != 0:
        if   facing == 0: here[1] += 1
        elif facing == 1: here[0] += 1
        elif facing == 2: here[1] -= 1
        else:             here[0] -= 1
        moves -= 1
        if (here[0], here[1]) not in visit:
            visit.append((here[0], here[1]))
        else:
            dx = fabs(origin[0] - here[0])
            dy = fabs(origin[1] - here[1])
            print("The Easter Bunny HQ is at " + str(int(dx + dy)) + " blocks away.")
            exit()
