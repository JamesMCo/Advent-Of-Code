#!/usr/bin/env python3

#Advent of Code
#2015 Day 8, Part 1
#Solution by James C. (https://github.com/JamesMCo)

f = open("puzzle_input.txt")
puzzle_input = f.read().split("\n")
f.close()

literals = 0
memory = 0

for i in puzzle_input[0:-1]:
    literals += len(i)
    memory += len(eval(i))

print("Characers of code in literal: " + str(literals))
print("Charaters of code in memory:  " + str(memory))
print("Literals - Memory = " + str(literals - memory))
