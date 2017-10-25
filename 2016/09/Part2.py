#!/usr/bin/env python3

#Advent of Code
#Day 9, Part 2
#Solution by /u/rhardih (https://reddit.com/r/adventofcode/comments/5hbygy/-/dazentu/)
#Implementation by James C. (https://github.com/JamesMCo)
#Gosh darn, I'm annoyed I couldn't figure out a solution myself :(

f = open("puzzle_input.txt")
puzzle_input = f.read()[:-1].replace(" ", "")
f.close()

weights = [1 for i in puzzle_input]
length = 0
i = 0
while i < len(puzzle_input):
    if puzzle_input[i] == "(":
        l = int(puzzle_input[i+1:].split("x")[0])
        r = int(puzzle_input[i+1:].split("x")[1].split(")")[0])
        for x in range(i+len(str(l))+len(str(r))+3, i+len(str(l))+len(str(r))+l+3):
            weights[x] = weights[x] * r
        i += len(str(l))+len(str(r))+3
    else:
        length += weights[i]
        i += 1

print("The decompressed length of the file is " + str(length) + ".")
