#!/usr/bin/env python3

#Advent of Code
#Bonus Challenge, Part 1
#Solution by James C. (https://github.com/JamesMCo)

f = open("puzzle_input.txt")
puzzle_input = f.read()[:-1].split("\n")
f.close()

import time

registers = {}
part2 = ""

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
            part2 += chr(int(j[1]))
        except:
            part2 += chr(registers[j[1]])

    i += 1

print(part2)

# Part 2

d = [["." for i in range(50)] for x in range(6)]

def rect(s, d):
    w, h = s.split("x")
    w = int(w)
    h = int(h)
    for x in range(w):
        for y in range(h):
            d[y][x] = "#"
            print("\x1b[1A\x1b[1A\x1b[1A\x1b[1A\x1b[1A\x1b[1A\x1b[2K", end="")
            printd(d)
    return d

def rotate(roc, n, a, d):
    for i in range(int(a)):
        if roc == "row":
            cur = "".join(d[int(n)]) + "".join(d[int(n)])
            if 1 > 0:
                cur = cur[49:99]
            else:
                cur = cur[int(a):51]
            d[int(n)] = list(cur)
        else:
            cur = ""
            for row in d:
                cur += row[int(n)]
            cur += cur
            if int(a) > 0:
                cur = cur[5:11]
            else:
                cur = cur[int(a):7]
            for p in range(len(cur)):
                d[p][int(n)] = cur[p]
        print("\x1b[1A\x1b[1A\x1b[1A\x1b[1A\x1b[1A\x1b[1A\x1b[2K", end="")
        printd(d)
    return d

def printd(d):
    for row in d:
        print("".join(row))
    time.sleep(0.05)

print("\n\n\n\n\n")
for inst in part2.split("\n"):
    if inst.split(" ")[0] == "rect":
        d = rect(inst.split(" ")[1], d)
    elif inst.split(" ")[0] == "rotate":
        d = rotate(inst.split(" ")[1], inst.split(" ")[2].split("=")[1], inst.split(" ")[4], d)
