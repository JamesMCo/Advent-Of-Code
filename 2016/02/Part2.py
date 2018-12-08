#!/usr/bin/env python3

#Advent of Code
#2016 Day 2, Part 2
#Solution by James C. (https://github.com/JamesMCo)

f = open("puzzle_input.txt")
puzzle_input = f.read().split("\n")
f.close()

here = [1, 1]
buttons = [[None, None, 5, None, None], [None, 2, 6, "A", None], [1, 3, 7, "B", "D"], [None, 4, 8, "C", None], [None, None, 9, None, None]]
code = ""

for l in puzzle_input:
    if l == "": continue
    for d in l:
        if d == "U" and here[1] != 0 and buttons[here[0]][here[1] - 1] != None:
            here[1] -= 1
        elif d == "D" and here[1] != 4 and buttons[here[0]][here[1] + 1] != None:
            here[1] += 1
        elif d == "L" and here[0] != 0 and buttons[here[0] - 1][here[1]] != None:
            here[0] -= 1
        elif d == "R" and here[0] != 4 and buttons[here[0] + 1][here[1]] != None:
            here[0] += 1
    code += str(buttons[here[0]][here[1]])

print("The code for the bathroom is " + code + ".")
