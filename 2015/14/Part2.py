#!/usr/bin/env python3

#Advent of Code
#Day 14, Part 2
#Solution by James C. (https://github.com/JamesMCo)

f = open("puzzle_input.txt")
puzzle_input = f.read().strip().split("\n")
f.close()

duration = 2503
stats = []
for reindeer in puzzle_input:
        reindeer = reindeer.split()

        stats.append({"t": 0,
                      "d": 0,
                      "speed": int(reindeer[3]),
                      "flytime": int(reindeer[6]),
                      "resttime": int(reindeer[13]),
                      "state": "fly",
                      "points": 0})

for second in range(duration):
    for i in range(len(stats)):
        if stats[i]["state"] == "fly":
            stats[i]["d"] += stats[i]["speed"]
            stats[i]["t"] += 1
            if stats[i]["t"] == stats[i]["flytime"]:
                stats[i]["t"] = 0
                stats[i]["state"] = "rest"

        elif stats[i]["state"] == "rest":
            stats[i]["t"] += 1
            if stats[i]["t"] == stats[i]["resttime"]:
                stats[i]["t"] = 0
                stats[i]["state"] = "fly"

    first = max(reindeer["d"] for reindeer in stats)
    for i in range(len(stats)):
        if stats[i]["d"] == first:
            stats[i]["points"] += 1

print("After " + str(duration) + " seconds, the winning reindeer has " + str(max(reindeer["points"] for reindeer in stats)) + " points.")