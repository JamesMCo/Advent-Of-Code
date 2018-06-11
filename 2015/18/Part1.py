#!/usr/bin/env python3

#Advent of Code
#Day 18, Part 1
#Solution by James C. (https://github.com/JamesMCo)

f = open("puzzle_input.txt")
puzzle_input = f.read().split("\n")[:-1]
f.close()

current = puzzle_input
working = []

def count_surrounding(x, y, current):
    c = 0
    l = len(current[0]) - 1

    if y > 0:
        if x > 0:
            c += int(current[y-1][x-1] == "#")
        c += int(current[y-1][x] == "#")
        if x < l:
            c += int(current[y-1][x+1] == "#")

    if x > 0:
        c += int(current[y][x-1] == "#")
    if x < l:
        c += int(current[y][x+1] == "#")

    if y < l:
        if x > 0:
            c += int(current[y+1][x-1] == "#")
        c += int(current[y+1][x] == "#")
        if x < l:
            c += int(current[y+1][x+1] == "#")

    return c

for step in range(100):
    for y, row in enumerate(current):
        working.append("")

        for x, col in enumerate(row):
            c = count_surrounding(x, y, current)
            if col == "#":
                if c in [2, 3]:
                    working[-1] += "#"
                else:
                    working[-1] += "."
            else:
                if c == 3:
                    working[-1] += "#"
                else:
                    working[-1] += "."   

    current = working[:]
    working = []

print("After 100 steps, the number of lights on is " + str(sum(x.count("#") for x in current)) + ".")