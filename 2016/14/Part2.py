#!/usr/bin/env python3

#Advent of Code
#Day 14, Part 2
#Solution by James C. (https://github.com/JamesMCo)

f = open("puzzle_input.txt")
puzzle_input = f.read()[:-1]
f.close()

from hashlib import md5

keys = 0
i = 0

hashes = {}

def stretch(s):
    global hashes

    if s not in hashes:
        temp = md5(str(s).encode("utf-8")).hexdigest()

        for i in range(2016):
            temp = md5(str(temp).encode("utf-8")).hexdigest()

        hashes[s] = temp
    return hashes[s]

while keys < 64:
    current_hash = stretch(puzzle_input + str(i))
    for c in range(len(current_hash)):
        try:
            if current_hash[c] == current_hash[c+1] == current_hash[c+2]:
                for j in range(1, 1001):
                    if current_hash[c]*5 in stretch(puzzle_input + str(i+j)):
                        keys += 1
                        break
                break
        except:
            pass
    i += 1

i -= 1
print("The index that generates the 64th key is " + str(i) + ".")
