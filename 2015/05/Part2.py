#!/usr/bin/env python3

#Advent of Code
#2015 Day 5, Part 2
#Solution by James C. (https://github.com/JamesMCo)

f = open("puzzle_input.txt")
puzzle_input = f.read().split("\n")
f.close()

nice = 0

for i in puzzle_input[0:-1]:
    pairs = False
    gap = False

    for x in range(len(i) - 1):
        if i.count(i[x:x+2]) > 1:
            pairs = True

    for x in range(len(i) - 2):
        if i[x] == i[x+2]:
            gap = True

    if pairs == True and gap == True:
        nice += 1

print("There are " + str(nice) + " nice strings.")
