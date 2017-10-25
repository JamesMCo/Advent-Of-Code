#!/usr/bin/env python3

#Advent of Code
#Bonus Challenge, Part 1
#Solution by James C. (https://github.com/JamesMCo)

f = open("puzzle_input_part1.txt")
puzzle_input = f.read()[:-1].split("\n")
f.close()

registers = {}

i = 0
while i < len(puzzle_input):
    j = puzzle_input[i].split(" ")

    #print("i=" + str(i))
    #print("j=" + " ".join(j))
    #print(registers)
    
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
                try:
                    int(j[2])
                    i += int(j[2]) - 1
                except:
                    i += registers[j[2]] - 1
        except:
            if j[1] in registers and registers[j[1]] != 0 and j[2] != 0:
                i += int(j[2]) - 1
    elif j[0] == "out":
        try:
            int(j[1])
            print(chr(int(j[1])), end="")
        except:
            print(chr(registers[j[1]]), end="")

    #input()
    i += 1
