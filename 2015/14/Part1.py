#!/usr/bin/env python3

#Advent of Code
#Day 14, Part 1
#Solution by James C. (https://github.com/JamesMCo)

f = open("puzzle_input.txt")
puzzle_input = f.read().strip().split("\n")
f.close()

duration = 2503
distances = []
for reindeer in puzzle_input:
    reindeer = reindeer.split()

    t = 0
    d = 0
    speed = int(reindeer[3])
    flytime = int(reindeer[6])
    resttime = int(reindeer[13])
    state = "fly"

    while t + flytime < duration:
        if state == "fly":
            d += speed * flytime
            t += flytime
            state = "rest"
        elif state == "rest":
            t += resttime
            state = "fly"

    if state == "fly" and t < duration:
        d += speed * (duration - t)
    distances.append(d)

print("After " + str(duration) + " seconds, the winning reindeer has travelled " + str(max(distances)) + "km.")