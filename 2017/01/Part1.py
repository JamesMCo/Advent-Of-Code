#!/usr/bin/env python3

#Advent of Code
#Day 1, Part 1
#Solution by James C. (https://github.com/JamesMCo)

f = open("puzzle_input.txt")
puzzle_input = f.read()[:-1]
f.close()

total = 0

for i, x in enumerate(puzzle_input):
    if puzzle_input[i] == puzzle_input[(i+1) % len(puzzle_input)]:
        total += int(x)

print("The solution to the captcha is " + str(total) + ".")
