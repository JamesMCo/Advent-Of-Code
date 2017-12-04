#!/usr/bin/env python3

#Advent of Code
#Day 4, Part 1
#Solution by James C. (https://github.com/JamesMCo)

f = open("puzzle_input.txt")
puzzle_input = f.read()[:-1].split("\n")
f.close()

count = 0

for passphrase in puzzle_input:
    words = passphrase.split(" ")
    if sorted(words) == sorted(set(words)):
        count += 1

print("The number of valid passphrases is " + str(count) + ".")
