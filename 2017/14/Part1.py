#!/usr/bin/env python3

#Advent of Code
#Day 14, Part 1
#Solution by James C. (https://github.com/JamesMCo)

import unittest

def knot(puzzle_input):
    def rotate(l, n):
        t = [x for x in l]
        if len(t) <= 1:
            return t
        if len(t) == 2:
            return t[1] + t[0]
        for i in range(n):
            t = t[1:] + [t[0]]
        return t
    
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

def solve(puzzle_input):
    base = puzzle_input + "-"
    grid = []
    used = 0

    for i in range(128):
        grid.append(bin(int(knot(base + str(i)), 16))[2:])

    for row in grid:
        used += row.count("1")
    
    return used

def main():
    f = open("puzzle_input.txt")
    puzzle_input = f.read()[:-1]
    f.close()

    used = solve(puzzle_input)

    print("The number of squares used is " + str(used) + ".")

class AOC_Tests(unittest.TestCase):
    def test_ex1(self):
        self.assertEqual(solve("flqrgnkx"), 8108)

if __name__ == "__main__":
    if unittest.main(verbosity=2, exit=False).result.wasSuccessful():
        main()
        exit(0)
    else:
        exit(1)
