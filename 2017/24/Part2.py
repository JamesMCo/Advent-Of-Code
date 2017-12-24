#!/usr/bin/env python3

#Advent of Code
#Day 24, Part 2
#Solution by James C. (https://github.com/JamesMCo)

import unittest

def solve(puzzle_input):
    def find_largest(parts, start, cur_strength, cur_length):
        bridges = []

        if len(parts) == 0:
            return [cur_strength, cur_length]

        for i in range(len(parts)):
            if start in parts[i]:
                temp_s, temp_l = find_largest(parts[:i] + parts[i+1:], parts[i][not parts[i].index(start)], cur_strength + parts[i][0] + parts[i][1], cur_length + 1)
                bridges.append([temp_s, temp_l])

        if len(bridges) == 0:
            return [cur_strength, cur_length]

        bridges.sort(reverse=True, key=lambda x: x[1])
        return max([x for x in bridges if x[1] == bridges[0][1]])

    parts = [sorted([int(x.split("/")[0]), int(x.split("/")[1])]) for x in puzzle_input]

    return find_largest(parts, 0, 0, 0)[0]

def main():
    f = open("puzzle_input.txt")
    puzzle_input = f.read()[:-1].split("\n")
    f.close()

    strongest = solve(puzzle_input)

    print("The strength of the longest bridge is " + str(strongest) + ".")

class AOC_Tests(unittest.TestCase):
    def test_ex1(self):
        self.assertEqual(solve(["0/2",
                                "2/2",
                                "2/3",
                                "3/4",
                                "3/5",
                                "0/1",
                                "10/1",
                                "9/10"]), 19)

if __name__ == "__main__":
    if unittest.main(verbosity=2, exit=False).result.wasSuccessful():
        main()
        exit(0)
    else:
        exit(1)
