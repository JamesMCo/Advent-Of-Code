#!/usr/bin/env python3

#Advent of Code
#2016 Day 7, Part 2
#Solution by James C. (https://github.com/JamesMCo)

f = open("puzzle_input.txt")
puzzle_input = f.read()[:-1].split("\n")
f.close()

supported = 0

for line in puzzle_input:
    brackets = 0
    aba = []
    bab = []
    for i in range(len(line) - 2):
        if line[i] == "[":
            brackets += 1
        elif line[i] == "]":
            brackets -= 1
        elif brackets == 0 and line[i] != line[i+1] and line[i] == line[i+2]:
            if line[i] + line[i+1] + line[i+2] not in aba:
                aba.append(line[i] + line[i+1] + line[i+2])
        elif brackets > 0 and line[i] != line[i+1] and line[i] == line[i+2]:
            if line[i] + line[i+1] + line[i+2] not in bab:
                bab.append(line[i] + line[i+1] + line[i+2])
    for i in aba:
        if i[1] + i[0] + i[1] in bab:
            supported += 1
            break

print("The number of SSL supporting IPs is " + str(supported) + ".")
