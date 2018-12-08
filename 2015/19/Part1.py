#!/usr/bin/env python3

#Advent of Code
#2015 Day 18, Part 1
#Solution by James C. (https://github.com/JamesMCo)

f = open("puzzle_input.txt")
puzzle_input = f.read().strip().split("\n")
f.close()

base = puzzle_input[-1]
replacements = {}
for replacement in puzzle_input[:-2]:
    replacement = replacement.split()
    if replacement[0] not in replacements:
        replacements[replacement[0]] = [replacement[2]]
    else:
        replacements[replacement[0]].append(replacement[2])

longest = max(len(x) for x in replacements)
found = []
for i in range(len(base)):
    for j in range(1, longest+1):
        if i + j <= len(base):
            if base[i:i+j] in replacements:
                for case in replacements[base[i:i+j]]:
                    if base[:i] + case + base[i+j:] not in found:
                        found.append(base[:i] + case + base[i+j:])

print("The medicine molecule allows for " + str(len(found)) + " distinct molecules.")