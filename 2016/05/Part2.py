#!/usr/bin/env python3

#Advent of Code
#Day 5, Part 2
#Solution by James C. (https://github.com/JamesMCo)

f = open("puzzle_input.txt")
puzzle_input = f.read()[:-1]
f.close()

from hashlib import md5
from random import choice
from string import ascii_letters, punctuation

def printpass(replace=True):
    if replace: print("\x1b[1A\x1b[2K", end="")
    print("The password is ", end="")
    for i in password:
        if i != "_":
            print(i, end="")
        else:
            print(choice(ascii_letters + punctuation), end="")
    print(".")

password = ["_" for i in range(8)]
current_index = 0
printpass(False)

while "_" in password:
    current_hash = md5(str(puzzle_input + str(current_index)).encode("utf-8")).hexdigest()
    if len(current_hash) > 5 and current_hash[:5] == "0"*5 and 0 <= int(current_hash[5], 16) <= 7 and password[int(current_hash[5], 16)] == "_":
        password[int(current_hash[5], 16)] = current_hash[6]
        printpass()
        current_index += 1
        continue
    if current_index % 15000 == 0:
        printpass()
    current_index += 1
