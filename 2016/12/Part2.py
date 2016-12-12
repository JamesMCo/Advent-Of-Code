#!/usr/bin/env python3

#Advent of Code
#Day 12, Part 2
#Solution by Jammy4312 (https://jammy4312.me)

f = open("puzzle_input.txt")
puzzle_input = f.read()[:-1].split("\n")
f.close()

registers = {"c": 1}

i = 0
while i < len(puzzle_input):
    j = puzzle_input[i].split(" ")
    if j[0] == "cpy":
        try:
            int(j[1])
            registers[j[2]] = int(j[1])
        except:
            registers[j[2]] = registers[j[1]]
    elif j[0] == "inc":
        registers[j[1]] += 1
    elif j[0] == "dec":
        registers[j[1]] -= 1
    elif j[0] == "jnz":
        try:
            int(j[1])
            if j[1] != "0":
                i += int(j[2]) - 1
        except:
            if j[1] in registers and registers[j[1]] != 0 and j[2] != 0:
                i += int(j[2]) - 1
    i += 1

print("The value of register a is " + str(registers["a"]) + ".")
