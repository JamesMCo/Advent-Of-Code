#!/usr/bin/env python3

#Advent of Code
#Day 6, Part 1
#Solution by Jammy4312 (https://jammy4312.me)

f = open("puzzle_input.txt")
puzzle_input = f.read().split("\n")
f.close()

lights = [[0 for i in range(1000)] for i in range(1000)]
on = 0

for i in puzzle_input[0:-1]:
    if i.split(" ")[0:2] in [["turn", "off"], ["turn", "on"]]:
        for x in range(int(i.split(" ")[2].split(",")[0]), int(i.split(" ")[4].split(",")[0])+1):
            for y in range(int(i.split(" ")[2].split(",")[1]), int(i.split(" ")[4].split(",")[1])+1):
                if i.split(" ")[1] == "on":
                    lights[x][y] = 1
                else:
                    lights[x][y] = 0
    elif i.split(" ")[0] == "toggle":
        for x in range(int(i.split(" ")[1].split(",")[0]), int(i.split(" ")[3].split(",")[0])+1):
            for y in range(int(i.split(" ")[1].split(",")[1]), int(i.split(" ")[3].split(",")[1])+1):
                if lights[x][y] == 0:
                    lights[x][y] = 1
                else:
                    lights[x][y] = 0
    else:
        print("Problem!")

for x in lights:
    for y in x:
        if y == 1:
            on += 1

print("There are " + str(on) + " lights that are lit.")
