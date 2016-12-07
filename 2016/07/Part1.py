#!/usr/bin/env python3

#Advent of Code
#Day 7, Part 1
#Solution by Jammy4312 (https://jammy4312.me)

f = open("puzzle_input.txt")
puzzle_input = f.read()[:-1].split("\n")
f.close()

supported = 0

for line in puzzle_input:
    brackets = 0
    this_sup = False
    invalid  = False
    for i in range(len(line) - 3):
        if line[i] == "[":
            brackets += 1
        elif line[i] == "]":
            brackets -= 1
        elif brackets == 0 and line[i] != line[i+1] and line[i] + line[i+1] == line[i+3] + line[i+2]:
            this_sup = True
        elif brackets > 0 and line[i] != line[i+1] and line[i] + line[i+1] == line[i+3] + line[i+2]:
            invalid = True
    if not invalid:
        supported += this_sup

print("The number of TLS supporting IPs is " + str(supported) + ".")
