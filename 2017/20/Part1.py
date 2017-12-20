#!/usr/bin/env python3

#Advent of Code
#Day 20, Part 1
#Solution by James C. (https://github.com/JamesMCo)

import unittest

def solve(puzzle_input):
    accs = []
    for particle in puzzle_input:
        accs.append(sum(abs(int(x)) for x in particle.split("<")[3].split(">")[0].split(",")))

    return accs.index(min(accs))

def main():
    f = open("puzzle_input.txt")
    puzzle_input = f.read()[:-1].split("\n")
    f.close()

    particle = solve(puzzle_input)

    print("The particle that stays closest to <0,0,0> is " + str(particle) + ".")

class AOC_Tests(unittest.TestCase):
    def test_ex1(self):
        self.assertEqual(solve(["p=< 3,0,0>, v=< 2,0,0>, a=<-1,0,0>",
                                "p=< 4,0,0>, v=< 0,0,0>, a=<-2,0,0>"]), 0)

if __name__ == "__main__":
    if unittest.main(verbosity=2, exit=False).result.wasSuccessful():
        main()
        exit(0)
    else:
        exit(1)
