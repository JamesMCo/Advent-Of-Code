#!/usr/bin/env python3

#Advent of Code
#2016 Day 6, Part 2
#Solution by James C. (https://github.com/JamesMCo)

f = open("puzzle_input.txt")
puzzle_input = f.read()[:-1].split("\n")
f.close()

from collections import Counter

message = ""

for i in range(len(puzzle_input[0])):
    letters = [x[i] for x in puzzle_input]
    c = Counter(letters)
    message += c.most_common()[-1][0]

print("The message is " + message + ".")
