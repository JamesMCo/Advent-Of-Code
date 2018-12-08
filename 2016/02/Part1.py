#!/usr/bin/env python3

#Advent of Code
#2016 Day 2, Part 1
#Solution by James C. (https://github.com/JamesMCo)

f = open("puzzle_input.txt")
puzzle_input = f.read().split("\n")
f.close()

here = [1, 1]
buttons = [[1, 4, 7], [2, 5, 8], [3, 6, 9]]
code = ""

for l in puzzle_input:
    if l == "": continue
    for d in l:
        if d == "U" and here[1] != 0:
            here[1] -= 1
        elif d == "D" and here[1] != 2:
            here[1] += 1
        elif d == "L" and here[0] != 0:
            here[0] -= 1
        elif d == "R" and here[0] != 2:
            here[0] += 1
    code += str(buttons[here[0]][here[1]])

print("The code for the bathroom is " + code + ".")
