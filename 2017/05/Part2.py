#!/usr/bin/env python3

#Advent of Code
#Day 5, Part 2
#Solution by James C. (https://github.com/JamesMCo)

f = open("puzzle_input.txt")
puzzle_input = [int(x) for x in f.read()[:-1].split("\n")]
f.close()

i = 0
steps = 0
length = len(puzzle_input)

while 0 <= i < length:
    t = puzzle_input[i]
    if puzzle_input[i] >= 3:
        puzzle_input[i] -= 1
    else:
        puzzle_input[i] += 1
    i += t
    steps += 1

print("It takes " + str(steps) + " steps to reach the exit.")
