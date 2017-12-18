#!/usr/bin/env python3

#Advent of Code
#Day 18, Part 2
#Solution by James C. (https://github.com/JamesMCo)

import collections, unittest

def solve(puzzle_input):
    class Program:
        def __init__(self, id, puzzle_input):
            self.i = 0
            self.registers = [0 for x in range(26)]
            self.registers[15] = id
            self.queue = collections.deque()
            self.puzzle_input = puzzle_input

            self.waiting = False
            self.terminated = False
            self.sent = 0

            self.other   = None

        def receive(self, value):
            self.queue.append(value)

        def run(self):
            if self.i < len(self.puzzle_input) and not self.terminated:
                inst = self.puzzle_input[self.i].split()
                op   = inst[0]
                try:
                    reg = int(inst[1])
                    reg_num = True
                except:
                    reg  = ord(inst[1]) - 97
                    reg_num = False
                if len(inst) == 3:
                    if len(inst[2]) > 1:
                        val = int(inst[2])
                    else:
                        if 97 <= ord(inst[2]) <= 122:
                            val = self.registers[ord(inst[2]) - 97]
                        else:
                            val = int(inst[2])
                else:
                    val = None
                
                if op == "snd":
                    if reg_num:
                        self.other.receive(reg)
                    else:
                        self.other.receive(self.registers[reg])
                    self.sent += 1
                    self.i += 1
                elif op == "set":
                    self.registers[reg]  = val
                    self.i += 1
                elif op == "add":
                    self.registers[reg] += val
                    self.i += 1
                elif op == "mul":
                    self.registers[reg] *= val
                    self.i += 1
                elif op == "mod":
                    self.registers[reg] %= val
                    self.i += 1
                elif op == "rcv":
                    self.waiting = True
                    if len(self.queue) > 0:
                        self.registers[reg] = self.queue.popleft()
                        self.waiting = False
                        self.i += 1
                elif op == "jgz":
                    if self.registers[reg] > 0:
                        self.i += val
                    else:
                        self.i += 1
            else:
                self.terminated = True

    program0 = Program(0, puzzle_input)
    program1 = Program(1, puzzle_input)

    program0.other = program1
    program1.other = program0

    while True:
        if program0.waiting and program1.waiting:
            break
        if program0.terminated and program1.waiting:
            break
        if program0.waiting and program1.terminated:
            break
        if program0.terminated and program1.terminated:
            break

        program0.run()
        program1.run()


    return program1.sent

def main():
    f = open("puzzle_input.txt")
    puzzle_input = f.read()[:-1].split("\n")
    f.close()

    freq = solve(puzzle_input)

    print("Program 1 sent " + str(freq) + " values.")

class AOC_Tests(unittest.TestCase):
    def test_ex1(self):
        self.assertEqual(solve(["snd 1",
                                "snd 2",
                                "snd p",
                                "rcv a",
                                "rcv b",
                                "rcv c",
                                "rcv d"]), 3)

if __name__ == "__main__":
    if unittest.main(verbosity=2, exit=False).result.wasSuccessful():
        main()
        exit(0)
    else:
        exit(1)
