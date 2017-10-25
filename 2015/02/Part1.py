#!/usr/bin/env python3

#Advent of Code
#Day 2, Part 1
#Solution by James C. (https://github.com/JamesMCo)

f = open("puzzle_input.txt")
puzzle_input = f.read()
f.close()

total = 0

for i in puzzle_input.split("\n")[0:-1]:
    current = i.split("x")
    side1 = int(current[0]) * int(current[1])
    side2 = int(current[1]) * int(current[2])
    side3 = int(current[2]) * int(current[0])

    areas = [side1, side2, side3]
    areas.sort()
    total += 3 * areas[0]
    total += 2 * areas[1]
    total += 2 * areas[2]

print("The elves need " + str(total) + " square feet of wrapping paper.")
