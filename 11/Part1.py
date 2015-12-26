#!/usr/bin/env python3

#Advent of Code
#Day 11, Part 1
#Solution by Jammy4312 (https://jammy4312.me)

f = open("puzzle_input.txt")
puzzle_input = f.read()[0:-1]
f.close()

import string

class Increment(object):
    """A class to increment a string.

    e.g.
    a -> b
    b -> c
    c -> d
    z -> a"""

    def __init__(self, password):
        self.password = password

    def __iter__(self):
        return self

    def __next__(self):
        if self.password[7] != "z":
            self.password = self.password[0:7] + chr(ord(self.password[7]) + 1)
        elif self.password[6] != "z":
            self.password = self.password[0:6] + chr(ord(self.password[6]) + 1) + "a"
        elif self.password[5] != "z":
            self.password = self.password[0:5] + chr(ord(self.password[5]) + 1) + "aa"
        elif self.password[4] != "z":
            self.password = self.password[0:4] + chr(ord(self.password[4]) + 1) + "aaa"
        elif self.password[3] != "z":
            self.password = self.password[0:3] + chr(ord(self.password[3]) + 1) + "aaaa"
        elif self.password[2] != "z":
            self.password = self.password[0:2] + chr(ord(self.password[2]) + 1) + "aaaaa"
        elif self.password[1] != "z":
            self.password = self.password[0] + chr(ord(self.password[1]) + 1) + "aaaaaa"
        elif self.password[0] != "z":
            self.password = chr(ord(self.password[0]) + 1) + "aaaaaaa"
        else:
            raise StopIteration()
        return self.password

def check(password):
    """A function to check if the supplied password fits the requirements
    for Santa's passwords."""

    checks = [0, 1, 0]
    letters = string.ascii_lowercase

    for i, x in enumerate(letters[0:-2]):
        if x + letters[i+1] + letters[i+2] in password:
            checks[0] = 1

    for i in ["i", "o", "l"]:
        if i in password:
            checks[1] = 0

    for i in letters:
        if i*2 in password:
            if i*3 not in password:
                checks[2] += 1
            else:
                checks[2] = 0

    if checks[2] >= 2:
        checks[2] = 1
    else:
        checks[2] = 0

    return checks

print("Santa's current password is: " + puzzle_input[0:8])

def nextpassword(current, silence=False):
    for i in Increment(current):
        results = check(i)
        if sum(results) == 3:
            if silence == False:
                print("Santa's new password is: " + i)
            break

nextpassword(puzzle_input)
