#!/usr/bin/env python3

#Advent of Code
#Day 10, Part 2
#Solution by James C. (https://github.com/JamesMCo)

f = open("puzzle_input.txt")
puzzle_input = f.read()
f.close()

import itertools

def look_and_say(original, repeats):
    current = original
    for i in range(repeats):
        split = ["".join(grp) for num, grp in itertools.groupby(current)]
        new = ""
        for x in split:
            new += str(len(x))
            new += x[0]
        current = new
    return(current)

print("The final result is " + str(len(look_and_say(puzzle_input[0:-1], 50))) + " characters long.")
