#!/usr/bin/env python3

#Advent of Code
#Day 6, Part 2
#Solution by James C. (https://github.com/JamesMCo)

f = open("puzzle_input.txt")
puzzle_input = [int(x) for x in f.read()[:-1].split(" ") if x != ""]
f.close()

length = len(puzzle_input)
state = 2

while state:
    history = []
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
    state -= 1

print("The number of redistribution cycles in the infinite loop is " + str(len(history)) + ".")
