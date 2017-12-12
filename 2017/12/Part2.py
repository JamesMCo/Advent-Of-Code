#!/usr/bin/env python3

#Advent of Code
#Day 12, Part 2
#Solution by James C. (https://github.com/JamesMCo)

import unittest

def solve(puzzle_input):
    programs = {}
    connections = ["0"]
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

def main():
    f = open("puzzle_input.txt")
    puzzle_input = f.read()[:-1].split("\n")
    f.close()

    groups = solve(puzzle_input)

    print("The number of groups in the input is " + str(groups) + ".")

class AOC_Tests(unittest.TestCase):
    def test_ex1(self):
        self.assertEqual(solve(["0 <-> 2",
                                "1 <-> 1",
                                "2 <-> 0, 3, 4",
                                "3 <-> 2, 4",
                                "4 <-> 2, 3, 6",
                                "5 <-> 6",
                                "6 <-> 4, 5"]), 2)

if __name__ == "__main__":
    if unittest.main(verbosity=2, exit=False).result.wasSuccessful():
        main()
        exit(0)
    else:
        exit(1)
