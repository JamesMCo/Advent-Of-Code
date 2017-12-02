#!/usr/bin/env python3

#Advent of Code
#Day 2, Part 1
#Solution by James C. (https://github.com/JamesMCo)

f = open("puzzle_input.txt")
puzzle_input = f.read()[:-1].split("\n")
f.close()

checksum = 0

for row in puzzle_input:
    temp = [int(x) for x in row.split(" ") if x != ""]
    checksum += max(temp) - min(temp)


print("The checksum of the spreadsheet is " + str(checksum) + ".")
