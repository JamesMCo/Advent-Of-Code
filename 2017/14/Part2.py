#!/usr/bin/env python3

#Advent of Code
#Day 14, Part 2
#Solution by James C. (https://github.com/JamesMCo)

import unittest

def rotate(l, n):
    t = [x for x in l]
    if len(t) <= 1:
        return t
    if len(t) == 2:
        return t[1] + t[0]
    for i in range(n):
        t = t[1:] + [t[0]]
    return t

def knot(puzzle_input):
    puzzle_input = [ord(x) for x in puzzle_input] + [17,31,73,47,23]
    l = [x for x in range(256)]
    skip_size = 0
    total_rotations = 0

    for j in range(64):
        for i in puzzle_input:
            if i <= 256:
                l = l[i-1::-1] + l[i:]
            else:
                l = l[::-1]
            l = rotate(l, i + skip_size)
            total_rotations += i + skip_size
            skip_size += 1

    l = rotate(l, 256 - (total_rotations % 256))

    output = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    for i in range(256):
        if i % 16 == 0:
            output[int(i / 16)] = l[i]
        else:
            output[int(i / 16)] ^= l[i]
        i += 1
    return "".join(hex(x)[2:].zfill(2) for x in output)

def day12_p2(puzzle_input):
    programs = {}
    connections = [puzzle_input[0].split(" ")[0]]
    for p in puzzle_input:
        programs[p.split(" ")[0]] = " ".join(p.split(" ")[2:]).split(", ")

    groups = 0

    found = True
    while found:
        found = False
        groups += 1

        added = True
        while added:
            added = False
            for c in connections:
                for p in programs[c]:
                    if p not in connections:
                        connections.append(p)
                        added = True
        
        for p in programs:
            if p not in connections:
                connections.append(p)
                found = True
                break

    return groups

def solve(puzzle_input):
    base = puzzle_input + "-"
    grid = []
    d12_input = []

    for i in range(128):
        grid.append(bin(int(knot(base + str(i)), 16))[2:].zfill(128).replace("0", ".").replace("1", "#"))

    for y in range(128):
        for x in range(128):
            if grid[y][x] == "#":
                d12_input.append(f"[{x}|{y}] <-> ")
                if y != 0:
                    if grid[y-1][x] == "#":
                            d12_input[-1] += f"[{x}|{y-1}], "
                if x != 0:
                    if grid[y][x-1] == "#":
                        d12_input[-1] += f"[{x-1}|{y}], "
                d12_input[-1] += f"[{x}|{y}], "
                if x != 127:
                    if grid[y][x+1] == "#":
                        d12_input[-1] += f"[{x+1}|{y}], "
                if y != 127:
                    if grid[y+1][x] == "#":
                            d12_input[-1] += f"[{x}|{y+1}], "
                d12_input[-1] = d12_input[-1][:-2]

    return day12_p2(d12_input)

def main():
    f = open("puzzle_input.txt")
    puzzle_input = f.read()[:-1]
    f.close()

    regions = solve(puzzle_input)

    print("The number of regions in the grid is " + str(regions) + ".")

class AOC_Tests(unittest.TestCase):
    def test_ex1(self):
        self.assertEqual(solve("flqrgnkx"), 1242)

main()
# if __name__ == "__main__":
#     if unittest.main(verbosity=2, exit=False).result.wasSuccessful():
#         main()
#         exit(0)
#     else:
#         exit(1)
