#!/usr/bin/env python3

#Advent of Code
#Day 5, Part 1
#Solution by James C. (https://github.com/JamesMCo)

f = open("puzzle_input.txt")
puzzle_input = f.read()[:-1].split("\n")
f.close()

i = 0
steps = 0

while 0 <= i < len(puzzle_input):
    t = int(puzzle_input[i])
    puzzle_input[i] = t + 1
    i += t
    steps += 1

print("It takes " + str(steps) + " steps to reach the exit.")
