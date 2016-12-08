#!/usr/bin/env python3

#Advent of Code
#Day 8, Part 2, Animated
#Solution by Jammy4312 (https://jammy4312.me)

f = open("puzzle_input.txt")
puzzle_input = f.read()[:-1].split("\n")
f.close()

import time

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
for inst in puzzle_input:
    if inst.split(" ")[0] == "rect":
        d = rect(inst.split(" ")[1], d)
    elif inst.split(" ")[0] == "rotate":
        d = rotate(inst.split(" ")[1], inst.split(" ")[2].split("=")[1], inst.split(" ")[4], d)
