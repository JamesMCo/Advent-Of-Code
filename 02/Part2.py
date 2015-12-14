#!/usr/bin/env python3

#Advent of Code
#Day 2, Part 2
#Solution by Jammy4312 (https://jammy4312.me)

f = open("puzzle_input.txt")
puzzle_input = f.read()
f.close()

total = 0

for i in puzzle_input.split("\n")[0:-1]:
    current = i.split("x")
    side1 = 2 * int(current[0]) + 2 * int(current[1])
    side2 = 2 * int(current[1]) + 2 * int(current[2])
    side3 = 2 * int(current[2]) + 2 * int(current[0])

    perimeters = [side1, side2, side3]
    perimeters.sort()
    total += perimeters[0]
    total += int(current[0]) * int(current[1]) * int(current[2])

print("The elves need " + str(total) + " feet of ribbon.")
