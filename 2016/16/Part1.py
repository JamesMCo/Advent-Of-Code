#!/usr/bin/env python3

#Advent of Code
#Day 16, Part 1
#Solution by James C. (https://github.com/JamesMCo)

f = open("puzzle_input.txt")
puzzle_input = f.read()[:-1]
f.close()

required_length = 272
state = puzzle_input

def step(a):
    return a + "0" + a[::-1].replace("1", "-").replace("0", "1").replace("-", "0")

def checksum(a):
    o = ""
    for i in range(0, len(a)-1, 2):
        if a[i] == a[i+1]:
            o += "1"
        else:
            o += "0"
    if len(o) % 2 == 0:
        return checksum(o)
    return o

while len(state) < required_length:
    state = step(state)

print("The correct checksum is " + checksum(state[:required_length]))