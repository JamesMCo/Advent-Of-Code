#!/usr/bin/env python3

#Advent of Code
#2019 Day 23, Part 1
#Solution by James C. (https://github.com/JamesMCo)

import os, sys
sys.path.append(os.path.abspath("../.."))
import unittest, util.read
from util.tests import run

from collections import deque
import typing as t
from util.intcode_2019 import IntcodeComputer

def solve(puzzle_input):
    class Ether:
        computers: dict[int, IntcodeComputer]
        packet_queue: dict[int, deque[tuple[int, int]]]

        def __init__(self: t.Self):
            self.computers = {
                network_address: IntcodeComputer().load_memory(puzzle_input).queue_inputs(network_address)
                for network_address in range(50)
            }
            self.packet_queue = {network_address: deque() for network_address in range(50)}

        def step(self: t.Self) -> t.Optional[int]:
            for network_address, computer in self.computers.items():
                if computer.waiting_for_input():
                    if self.packet_queue[network_address]:
                        computer.queue_inputs(self.packet_queue[network_address].popleft())
                    else:
                        computer.queue_inputs(-1)

                computer.step()

                if len(computer.outputs) == 3:
                    destination, x, y = computer.outputs
                    if destination == 255:
                        return y
                    self.packet_queue[destination].append((x, y))
                    computer.outputs.clear()

            return None

    ether = Ether()
    while True:
        if result := ether.step():
            return result

def main():
    puzzle_input = util.read.as_int_list(",")

    y = solve(puzzle_input)

    print("The y value of the first packet sent to address 255 is " + str(y) + ".")

class AOC_Tests(unittest.TestCase):
    @unittest.skip("No test cases")
    def test_ex1(self):
        pass

if __name__ == "__main__":
    run(main)
