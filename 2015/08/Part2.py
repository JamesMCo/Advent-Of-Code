#!/usr/bin/env python3

#Advent of Code
#Day 8, Part 2
#Solution by James C. (https://github.com/JamesMCo)

f = open("puzzle_input.txt")
puzzle_input = f.read().split("\n")
f.close()

literals = 0
encoded = 0

for i in puzzle_input[0:-1]:
    literals += len(i)
    encoded += len("\""+i.replace('"', '/"').replace("\\", "\\\\").replace("/", "\\")+"\"")

print("Characers of code in encoding: " + str(encoded))
print("Charaters of code in literals: " + str(literals))
print("Encoded - Literals = " + str(encoded - literals))
