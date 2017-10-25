#!/usr/bin/env python3

#Advent of Code
#Day 1, Part 2
#Solution by James C. (https://github.com/JamesMCo)

f = open("puzzle_input.txt")
puzzle_input = f.read()
f.close()

floor = 0

for i, x in enumerate(puzzle_input):
    if x == "(":
        floor += 1
    else:
        floor -= 1
    if floor < 0:
        print("The first character that causes Santa to enter the basement is character " + str(i+1) + ".")
        break
