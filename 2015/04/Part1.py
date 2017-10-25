#!/usr/bin/env python3

#Advent of Code
#Day 4, Part 1
#Solution by James C. (https://github.com/JamesMCo)

f = open("puzzle_input.txt")
puzzle_input = f.read().split("\n")[0]
f.close()

import hashlib

i = 0
while True:
    current_hash = hashlib.md5(str(puzzle_input + str(i)).encode("utf-8")).hexdigest()
    if current_hash[0:5] == "00000":
        break
    print("Tried " + str(i) + ", returned: " + current_hash)
    i += 1

print("Tried " + str(i) + ", returned: " + current_hash)
print("The lowest positive integer to produce a hash is: " + str(i) + ".")
