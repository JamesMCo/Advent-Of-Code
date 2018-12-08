#!/usr/bin/env python3

#Advent of Code
#2015 Day 5, Part 1
#Solution by James C. (https://github.com/JamesMCo)

f = open("puzzle_input.txt")
puzzle_input = f.read().split("\n")
f.close()

nice = 0

for i in puzzle_input[0:-1]:
    vowels = 0
    vowels += list(i).count("a")
    vowels += list(i).count("e")
    vowels += list(i).count("i")
    vowels += list(i).count("o")
    vowels += list(i).count("u")

    doubles = False
    for x in range(97, 123):
        if chr(x)*2 in i:
            doubles = True

    badstring = False
    for x in ["ab", "cd", "pq", "xy"]:
        if x in i:
            badstring = True

    if vowels >= 3 and doubles == True and badstring == False:
        nice += 1

print("There are " + str(nice) + " nice strings.")
