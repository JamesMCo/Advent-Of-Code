#!/usr/bin/env python3

#Advent of Code
#Day 6, Part 1
#Solution by James C. (https://github.com/JamesMCo)

f = open("puzzle_input.txt")
puzzle_input = [int(x) for x in f.read()[:-1].split(" ") if x != ""]
f.close()

history = []
length = len(puzzle_input)

while str(puzzle_input) not in history:
    history.append(str(puzzle_input))
    i = j = puzzle_input.index(max(puzzle_input))
    c = puzzle_input[i]
    puzzle_input[j] = 0
    j = (i + 1) % length
    while c > 0:
        puzzle_input[j] += 1
        c -= 1
        j = (j + 1) % length

print("The number of redistribution cycles required before repeats is " + str(len(history)) + ".")
