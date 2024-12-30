#!/usr/bin/env python3

#Advent of Code
#2021 Day 16, Part 2
#Solution by James C. (https://github.com/JamesMCo)

import os, sys
sys.path.append(os.path.abspath("../.."))
import unittest, util.read
from util.tests import run

from functools import reduce
from math import prod

def solve(puzzle_input):
    class Packet:
        def __init__(self, bits, offset=0):
            self.version = int(bits[offset+0:offset+3], 2)
            self.type    = int(bits[offset+3:offset+6], 2)
            
            self.value = None
            self.sub_packets = []

            match self.type:
                case 4:
                    binary_repr = ""
                    i = offset + 6
                    while bits[i] == "1":
                        binary_repr += bits[i+1:i+5]
                        i += 5
                    binary_repr += bits[i+1:i+5]
                    self.value = int(binary_repr, 2)
                    self.bit_length = 1 + (i + 4 - offset)
                case operator:
                    length_type_id = bits[offset+6]
                    match length_type_id:
                        case "0":
                            total_bits = int(bits[offset+7:offset+22], 2)
                            inner_offset = 22
                            while inner_offset - 22 < total_bits:
                                p = Packet(bits, offset+inner_offset)
                                self.sub_packets.append(p)
                                inner_offset += p.bit_length
                            self.bit_length = 22 + total_bits
                        case "1":
                            total_packets = int(bits[offset+7:offset+18], 2)
                            inner_offset = 18
                            for i in range(total_packets):
                                p = Packet(bits, offset+inner_offset)
                                self.sub_packets.append(p)
                                inner_offset += p.bit_length
                            self.bit_length = 18 + sum(p.bit_length for p in self.sub_packets)

                    match operator:
                        case 0:
                            self.value = sum(p.value for p in self.sub_packets)
                        case 1:
                            self.value = prod(p.value for p in self.sub_packets)
                        case 2:
                            self.value = min(p.value for p in self.sub_packets)
                        case 3:
                            self.value = max(p.value for p in self.sub_packets)
                        case 5:
                            self.value = int(self.sub_packets[0].value > self.sub_packets[1].value)
                        case 6:
                            self.value = int(self.sub_packets[0].value < self.sub_packets[1].value)
                        case 7:
                            self.value = int(self.sub_packets[0].value == self.sub_packets[1].value)

        def version_sum(self):
            return self.version + sum(p.version_sum() for p in self.sub_packets)

    def hextobin(h):
        digits = {"0": "0000",
                  "1": "0001",
                  "2": "0010",
                  "3": "0011",
                  "4": "0100",
                  "5": "0101",
                  "6": "0110",
                  "7": "0111",
                  "8": "1000",
                  "9": "1001",
                  "A": "1010",
                  "B": "1011",
                  "C": "1100",
                  "D": "1101",
                  "E": "1110",
                  "F": "1111"}
        return reduce(str.__add__, map(lambda c: digits[c], h))

    return Packet(hextobin(puzzle_input)).value

def main():
    puzzle_input = util.read.as_string()

    value = solve(puzzle_input)

    print("The value of the packet is " + str(value) + ".")

class AOC_Tests(unittest.TestCase):
    def test_ex1(self):
        return self.assertEqual(solve("C200B40A82"), 3)

    def test_ex2(self):
        return self.assertEqual(solve("04005AC33890"), 54)

    def test_ex3(self):
        return self.assertEqual(solve("880086C3E88112"), 7)

    def test_ex4(self):
        return self.assertEqual(solve("CE00C43D881120"), 9)

    def test_ex5(self):
        return self.assertEqual(solve("D8005AC2A8F0"), 1)

    def test_ex6(self):
        return self.assertEqual(solve("F600BC2D8F"), 0)

    def test_ex7(self):
        return self.assertEqual(solve("9C005AC2F8F0"), 0)

    def test_ex8(self):
        return self.assertEqual(solve("9C0141080250320F1802104A08"), 1)

if __name__ == "__main__":
    run(main)
