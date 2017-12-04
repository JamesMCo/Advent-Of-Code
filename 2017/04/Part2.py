#!/usr/bin/env python3

#Advent of Code
#Day 4, Part 2
#Solution by James C. (https://github.com/JamesMCo)

from itertools import permutations

f = open("puzzle_input.txt")
puzzle_input = f.read()[:-1].split("\n")
f.close()

count = 0

for passphrase in puzzle_input:
    words = passphrase.split(" ")
    if sorted(words) == sorted(set(words)):
        invalid = False
        for i in words:
            for perm in permutations(i):
                if "".join(perm) != i and "".join(perm) in words:
                    invalid = True
                    break
            if invalid:
                break
        if not invalid:
            count += 1

print("The number of valid passphrases is " + str(count) + ".")
