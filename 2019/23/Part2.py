#!/usr/bin/env python3

#Advent of Code
#2019 Day 23, Part 2
#Solution by James C. (https://github.com/JamesMCo)

import os, sys
sys.path.append(os.path.abspath("../.."))
import unittest, util.read
from util.tests import run

from collections import deque
import typing as t
from util.intcode_2019 import IntcodeComputer

def solve(puzzle_input):
    class NAT:
        network: "Ether"
        packet: tuple[int, int]
        prev_sent_y: t.Optional[int]

        def __init__(self: t.Self, network: "Ether") -> None:
            self.network = network
            self.packet = (-1000, -1000)
            self.prev_sent_y = None

        def receive_packet(self: t.Self, packet: tuple[int, int]) -> None:
            self.packet = packet

        def check_idle(self: t.Self) -> t.Optional[int]:
            if all(self.network.idle_status.values()) and not any(self.network.packet_queue.values()):
                # All computers are idle and have no incoming packets
                if self.prev_sent_y == self.packet[1]:
                    return self.packet[1]

                self.network.packet_queue[0].append(self.packet)
                self.prev_sent_y = self.packet[1]

    class Ether:
        computers: dict[int, IntcodeComputer]
        packet_queue: dict[int, deque[tuple[int, int]]]
        idle_status: dict[int, bool]
        nat: NAT

        def __init__(self: t.Self):
            self.computers = {
                network_address: IntcodeComputer().load_memory(puzzle_input).queue_inputs(network_address)
                for network_address in range(50)
            }
            self.packet_queue = {network_address: deque() for network_address in range(50)}
            self.idle_status = {network_address: False for network_address in range(50)}
            self.nat = NAT(self)

        def step(self: t.Self) -> t.Optional[int]:
            for network_address, computer in self.computers.items():
                if computer.waiting_for_input():
                    if self.packet_queue[network_address]:
                        computer.queue_inputs(self.packet_queue[network_address].popleft())
                        self.idle_status[network_address] = False
                    else:
                        computer.queue_inputs(-1)
                        self.idle_status[network_address] = True

                computer.step()

                if len(computer.outputs) == 3:
                    destination, x, y = computer.outputs
                    if destination == 255:
                        self.nat.receive_packet((x, y))
                    else:
                        self.packet_queue[destination].append((x, y))
                    computer.outputs.clear()

            return self.nat.check_idle()

    ether = Ether()
    while True:
        if result := ether.step():
            return result

def main():
    puzzle_input = util.read.as_int_list(",")

    y = solve(puzzle_input)

    print("The first y value sent to address 0 twice in a row is " + str(y) + ".")

class AOC_Tests(unittest.TestCase):
    @unittest.skip("No test cases")
    def test_ex1(self):
        pass

run(main)
