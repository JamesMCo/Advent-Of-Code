#!/usr/bin/env python3

#Advent of Code
#2021 Day 24, Part 2
#Solution by James C. (https://github.com/JamesMCo)

import os, sys
sys.path.append(os.path.abspath("../.."))
import unittest, util.read
from util.tests import run

def solve(puzzle_input):
    class ALU:
        def __init__(self, w=0, x=0, y=0, z=0):
            self.vars = {"w": w, "x": x, "y": y, "z": z}
            self.input_buffer = []

        def run_inst(self, inst):
            match inst.split():
                case ("inp", a):
                    self.vars[a] = self.input_buffer.pop(0)
                case ("add", a, b):
                    try:
                        int(b)
                        self.vars[a] = self.vars[a] + int(b)
                    except ValueError:
                        self.vars[a] = self.vars[a] + self.vars[b]
                case ("mul", a, b):
                    try:
                        int(b)
                        self.vars[a] = self.vars[a] * int(b)
                    except ValueError:
                        self.vars[a] = self.vars[a] * self.vars[b]
                case ("div", a, b):
                    try:
                        int(b)
                        self.vars[a] = int(self.vars[a] / int(b))
                    except ValueError:
                        self.vars[a] = int(self.vars[a] / self.vars[b])
                case ("mod", a, b):
                    try:
                        int(b)
                        self.vars[a] = self.vars[a] % int(b)
                    except ValueError:
                        self.vars[a] = self.vars[a] % self.vars[b]
                case ("eql", a, b):
                    try:
                        int(b)
                        self.vars[a] = int(self.vars[a] == int(b))
                    except ValueError:
                        self.vars[a] = int(self.vars[a] == self.vars[b])

    # ######################################################### #
    #  Working out                                              #
    #  These functions aren't called, but were                  #
    #  used to try to understand the algorithm                  #
    #  (as well as a *lot* of reading tips from the subreddit)  #
    # ######################################################### #

    def manual_step(w, z, value_a, value_b):
        # Implements one step of the algorithm followed by puzzle_input directly
        x = z % 26
        if value_a < 0:
            z = int(z / 26)
        if (x + value_a) != w:
            z *= 26
            z += w + value_b
        return z

    def reimplemented_step(w, z, value_a, value_b):
        # Implements one step of the algorithm followed by puzzle_input using a stack
        x = z[-1] if z else 0
        if value_a < 0:
            z.pop()
        if (x + value_a) != w: # at F: ((INPUT + 14) - 10 == NEWINPUT)
            z.append(w + value_b)
        return z

    # #################### #
    #  End of working out  #
    # #################### #


    def matches_constraints(n):
        # Based on notes from working out:
        # https://github.com/JamesMCo/Advent-Of-Code/blob/master/2021/24/notes.txt

        digits = {chr(65+i): int(x) for i, x in enumerate(str(n))}
        return digits["E"] + 4 == digits["F"] and\
               digits["G"] + 2 == digits["H"] and\
               digits["D"] + 8 == digits["I"] and\
               digits["J"]     == digits["K"] and\
               digits["C"] - 5 == digits["L"] and\
               digits["B"] + 7 == digits["M"] and\
               digits["A"] - 1 == digits["N"]

    candidate_answers = []
    for a in range(2, 10):
        for b in range(1, 3):
            for c in range(6, 10):
                for d in range(1, 2):
                    for e in range(1, 6):
                        for g in range(1, 8):
                            for j in range(1, 10):
                                candidate = int(f"{a}{b}{c}{d}{e}{e+4}{g}{g+2}{d+8}{j}{j}{c-5}{b+7}{a-1}")
                                if matches_constraints(candidate):
                                    candidate_answers.append(candidate)
    
    answer = min(candidate_answers)

    # Verify answer actually runs on ALU and returns 0
    value_a = [int(puzzle_input[i].split()[-1]) for i in range(5, 240, 18)]
    value_b = [int(puzzle_input[i].split()[-1]) for i in range(15, 250, 18)]
    alu = ALU()
    alu.input_buffer = [int(d) for d in str(answer)]
    for inst in puzzle_input:
        alu.run_inst(inst)
    if alu.vars["z"]:
        raise Exception("Answer does not return 0 when given to ALU")
    return answer

def main():
    puzzle_input = util.read.as_lines()

    modelno = solve(puzzle_input)

    print("The smallest model number accepted by MONAD is " + str(modelno) + ".")

class AOC_Tests(unittest.TestCase):
    @unittest.skip("No test cases")
    def test_ex1(self):
        pass

if __name__ == "__main__":
    run(main)
