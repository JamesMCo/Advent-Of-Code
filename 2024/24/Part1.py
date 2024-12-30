#!/usr/bin/env python3

#Advent of Code
#2024 Day 24, Part 1
#Solution by James C. (https://github.com/JamesMCo)

import os, sys
sys.path.append(os.path.abspath("../.."))
import unittest, util.read
from util.tests import run

from typing import Self

def solve(puzzle_input: list[str]) -> int:
    wires: dict[str, "Wire"] = {}
    z_wires: list["Wire"] = []

    class Wire:
        name: str
        active: bool | None
        gate: tuple[str, str, str] | None

        def __init__(self: Self, name: str, active: bool | None = None, gate: tuple[str, str, str] | None = None) -> None:
            self.name = name
            self.active = active
            self.gate = gate

            wires[self.name] = self

        def get_active(self: Self) -> bool:
            if self.active is None:
                match self.gate:
                    case a, "AND", b: self.active = wires[a].get_active() & wires[b].get_active()
                    case a, "OR", b:  self.active = wires[a].get_active() | wires[b].get_active()
                    case a, "XOR", b: self.active = wires[a].get_active() ^ wires[b].get_active()
            return self.active

    reading_fixed: bool = True
    for line in puzzle_input:
        if not line:
            reading_fixed = False
            continue

        line_parts: list[str] = line.split()

        if reading_fixed:
            Wire(name=line_parts[0][:-1], active=line_parts[1] == "1")
            if line_parts[0][0] == "z":
                z_wires.append(wires[line_parts[0][:-1]])
        else:
            Wire(name=line_parts[-1], gate=(line_parts[0], line_parts[1], line_parts[2]))
            if line_parts[-1][0] == "z":
                z_wires.append(wires[line_parts[-1]])
    z_wires.sort(key=lambda wire: wire.name, reverse=True)

    return int("".join("1" if z_wire.get_active() else "0" for z_wire in z_wires), 2)

def main() -> tuple[str, int]:
    puzzle_input = util.read.as_lines()

    return "The decimal number output on the wires starting with z is {}.", solve(puzzle_input)

class AOC_Tests(unittest.TestCase):
    def test_ex1(self):
        return self.assertEqual(solve(["x00: 1",
                                       "x01: 1",
                                       "x02: 1",
                                       "y00: 0",
                                       "y01: 1",
                                       "y02: 0",
                                       "",
                                       "x00 AND y00 -> z00",
                                       "x01 XOR y01 -> z01",
                                       "x02 OR y02 -> z02"]), 4)

    def test_ex2(self):
        return self.assertEqual(solve(["x00: 1",
                                       "x01: 0",
                                       "x02: 1",
                                       "x03: 1",
                                       "x04: 0",
                                       "y00: 1",
                                       "y01: 1",
                                       "y02: 1",
                                       "y03: 1",
                                       "y04: 1",
                                       "",
                                       "ntg XOR fgs -> mjb",
                                       "y02 OR x01 -> tnw",
                                       "kwq OR kpj -> z05",
                                       "x00 OR x03 -> fst",
                                       "tgd XOR rvg -> z01",
                                       "vdt OR tnw -> bfw",
                                       "bfw AND frj -> z10",
                                       "ffh OR nrd -> bqk",
                                       "y00 AND y03 -> djm",
                                       "y03 OR y00 -> psh",
                                       "bqk OR frj -> z08",
                                       "tnw OR fst -> frj",
                                       "gnj AND tgd -> z11",
                                       "bfw XOR mjb -> z00",
                                       "x03 OR x00 -> vdt",
                                       "gnj AND wpb -> z02",
                                       "x04 AND y00 -> kjc",
                                       "djm OR pbm -> qhw",
                                       "nrd AND vdt -> hwm",
                                       "kjc AND fst -> rvg",
                                       "y04 OR y02 -> fgs",
                                       "y01 AND x02 -> pbm",
                                       "ntg OR kjc -> kwq",
                                       "psh XOR fgs -> tgd",
                                       "qhw XOR tgd -> z09",
                                       "pbm OR djm -> kpj",
                                       "x03 XOR y03 -> ffh",
                                       "x00 XOR y04 -> ntg",
                                       "bfw OR bqk -> z06",
                                       "nrd XOR fgs -> wpb",
                                       "frj XOR qhw -> z04",
                                       "bqk OR frj -> z07",
                                       "y03 OR x01 -> nrd",
                                       "hwm AND bqk -> z03",
                                       "tgd XOR rvg -> z12",
                                       "tnw OR pbm -> gnj"]), 2024)

if __name__ == "__main__":
    run(main)
