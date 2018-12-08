#!/usr/bin/env python3

#Advent of Code
#2015 Day 25, Part 1
#Solution by James C. (https://github.com/JamesMCo)

f = open("puzzle_input.txt")
puzzle_input = f.read()[0:-1].split()
f.close()

row = int(puzzle_input[puzzle_input.index("row")+1][:-1])
col = int(puzzle_input[puzzle_input.index("column")+1][:-1])
codeno = 1 + sum(range(1, row)) + sum(range(row + 1, row + col))

code = 20151125
for i in range(codeno - 1):
    code = (code * 252533) % 33554393

print("The code from the manual is " + str(code) + ".")