#!/usr/bin/env python3

#Advent of Code
#2016 Day 5, Part 1
#Solution by James C. (https://github.com/JamesMCo)

f = open("puzzle_input.txt")
puzzle_input = f.read()[:-1]
f.close()

from hashlib import md5

characters_found = 0
password = ""
current_index = 0

while characters_found < 8:
    current_hash = md5(str(puzzle_input + str(current_index)).encode("utf-8")).hexdigest()
    if len(current_hash) > 5 and current_hash[:5] == "0"*5:
        password += current_hash[5]
        characters_found += 1
    current_index += 1

print("The password is " + password + ".")
