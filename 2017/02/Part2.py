#!/usr/bin/env python3

#Advent of Code
#Day 2, Part 2
#Solution by James C. (https://github.com/JamesMCo)

f = open("puzzle_input.txt")
puzzle_input = f.read()[:-1].split("\n")
f.close()

checksum = 0

for row in puzzle_input:
    temp = sorted([int(x) for x in row.split() if x != ""], reverse=True)
    found = False
    for i in range(len(temp)):
        for j in range(i + 1, len(temp)):
            if temp[i] % temp[j] == 0:
                checksum += int(temp[i] / temp[j])
                found = True
                break
        if found:
            break

print("The checksum of the spreadsheet is " + str(checksum) + ".")
