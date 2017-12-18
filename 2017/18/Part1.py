#!/usr/bin/env python3

#Advent of Code
#Day 18, Part 1
#Solution by James C. (https://github.com/JamesMCo)

import unittest

def solve(puzzle_input):
    i = 0
    last_sound = None
    registers = [0 for x in range(26)]

    while i < len(puzzle_input):
        inst = puzzle_input[i].split()
        op   = inst[0]
        reg  = ord(inst[1]) - 97
        if len(inst) == 3:
            if len(inst[2]) > 1:
                val = int(inst[2])
            else:
                if 97 <= ord(inst[2]) <= 122:
                    val = registers[ord(inst[2]) - 97]
                else:
                    val = int(inst[2])
        else:
            val = None
        
        if op == "snd":
            last_sound = registers[reg]
            i += 1
        elif op == "set":
            registers[reg]  = val
            i += 1
        elif op == "add":
            registers[reg] += val
            i += 1
        elif op == "mul":
            registers[reg] *= val
            i += 1
        elif op == "mod":
            registers[reg] %= val
            i += 1
        elif op == "rcv":
            if registers[reg] != 0:
                return last_sound
            i += 1
        elif op == "jgz":
            if registers[reg] > 0:
                i += val
            else:
                i += 1

    return None

def main():
    f = open("puzzle_input.txt")
    puzzle_input = f.read()[:-1].split("\n")
    f.close()

    freq = solve(puzzle_input)

    print("The value of the first recovered frequency is " + str(freq) + ".")

class AOC_Tests(unittest.TestCase):
    def test_ex1(self):
        self.assertEqual(solve(["set a 1",
                                "add a 2",
                                "mul a a",
                                "mod a 5",
                                "snd a",
                                "set a 0",
                                "rcv a",
                                "jgz a -1",
                                "set a 1",
                                "jgz a -2"]), 4)

if __name__ == "__main__":
    if unittest.main(verbosity=2, exit=False).result.wasSuccessful():
        main()
        exit(0)
    else:
        exit(1)
