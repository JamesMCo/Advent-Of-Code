#!/usr/bin/env python3

#Advent of Code
#Day 12, Part 2
#Solution by James C. (https://github.com/JamesMCo)

import json

f = open("puzzle_input.txt")
puzzle_input = f.read()[0:-1]
f.close()

def handle(o):
    if type(o) == type({}):
        output = 0
        red = False
        for element in o:
            if o[element] == "red":
                red = True
                break
            elif type(o[element]) == type(0):
                output += o[element]
            elif type(o[element]) in [type({}), type([])]:
                output += handle(o[element])

        if red:
            output = 0
        return output
    elif type(o) == type([]):
        output = 0
        for element in o:
            if type(element) == type(0):
                output += element
            elif type(element) in [type({}), type([])]:
                output += handle(element)

        return output

total = handle(json.loads(puzzle_input))

print("The final total is: " + str(total))
