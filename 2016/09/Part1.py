#!/usr/bin/env python3

#Advent of Code
#Day 9, Part 1
#Solution by Jammy4312 (https://jammy4312.me)

f = open("puzzle_input.txt")
puzzle_input = f.read()[:-1].replace(" ", "")
f.close()

i = 0
while i < len(puzzle_input):
    if puzzle_input[i] == "(":
        l = int(puzzle_input[i+1:].split("x")[0])
        r = int(puzzle_input[i+1:].split("x")[1].split(")")[0])
        puzzle_input = puzzle_input[:i] + ")".join(puzzle_input[i:].split(")")[1:])[:l] * r + ")".join(puzzle_input[i+1:].split(")")[1:])[l:]
        i += r*l
    else:
        i += 1

print("The decompressed length of the file is " + str(len(puzzle_input)) + ".")
