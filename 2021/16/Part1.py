#!/usr/bin/env python3

#Advent of Code
#2021 Day 16, Part 1
#Solution by James C. (https://github.com/JamesMCo)

import os, sys
sys.path.append(os.path.abspath("../.."))
import unittest, util.read
from util.tests import run

from functools import reduce

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

    return Packet(hextobin(puzzle_input)).version_sum()

def main():
    puzzle_input = util.read.as_string()

    version_sum = solve(puzzle_input)

    print("The version sum of the packet is " + str(version_sum) + ".")

class AOC_Tests(unittest.TestCase):
    def test_ex1(self):
        return self.assertEqual(solve("D2FE28"), 6)

    def test_ex2(self):
        return self.assertEqual(solve("38006F45291200"), 9)

    def test_ex3(self):
        return self.assertEqual(solve("EE00D40C823060"), 14)

    def test_ex4(self):
        return self.assertEqual(solve("8A004A801A8002F478"), 16)

    def test_ex5(self):
        return self.assertEqual(solve("620080001611562C8802118E34"), 12)

    def test_ex6(self):
        return self.assertEqual(solve("C0015000016115A2E0802F182340"), 23)

    def test_ex7(self):
        return self.assertEqual(solve("A0016C880162017C3686B18A3D4780"), 31)

run(main)
