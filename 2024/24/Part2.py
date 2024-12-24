#!/usr/bin/env python3

#Advent of Code
#2024 Day 24, Part 2
#Solution by James C. (https://github.com/JamesMCo)

import os, sys
sys.path.append(os.path.abspath("../.."))
import unittest, util.read
from util.tests import run

from itertools import zip_longest
from typing import Self

def solve(puzzle_input: list[str]) -> str:
    # Honestly, this solution is a bit of a mess. You can see what I transformed my part 1
    # solution into, as well as some commented out searching, up until line 199.
    # After that point, you can find my solution based on the write-ups by reddit
    # users /u/LxsterGames and /u/ElevatedUser, to whom I am incredibly thankful.

    wires: dict[str, "Wire"] = {}
    x_wires: list["Wire"] = []
    y_wires: list["Wire"] = []
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
                # print(f"{self.name} = {" ".join(self.gate)}")
                match self.gate:
                    case a, "AND", b: return wires[a].get_active() & wires[b].get_active()
                    case a, "OR", b:  return wires[a].get_active() | wires[b].get_active()
                    case a, "XOR", b: return wires[a].get_active() ^ wires[b].get_active()
#             print(f"{self.name} = {self.active}")
            return self.active

        def get_dependencies(self: Self) -> set[Self]:
            if self.active is None:
                return {self, wires[self.gate[0]], wires[self.gate[2]]} | wires[self.gate[0]].get_dependencies() | wires[self.gate[2]].get_dependencies()
            return {self}

    reading_fixed: bool = True
    for line in puzzle_input:
        if not line:
            reading_fixed = False
            continue

        line_parts: list[str] = line.split()

        if reading_fixed:
            Wire(name=line_parts[0][:-1], active=line_parts[1] == "1")
            match line_parts[0][0]:
                case "x": x_wires.append(wires[line_parts[0][:-1]])
                case "y": y_wires.append(wires[line_parts[0][:-1]])
                case "z": z_wires.append(wires[line_parts[0][:-1]])
        else:
            Wire(name=line_parts[-1], gate=(line_parts[0], line_parts[1], line_parts[2]))
            match line_parts[-1][0]:
                case "x": x_wires.append(wires[line_parts[-1]])
                case "y": y_wires.append(wires[line_parts[-1]])
                case "z": z_wires.append(wires[line_parts[-1]])
    x_wires.sort(key=lambda wire: wire.name, reverse=True)
    y_wires.sort(key=lambda wire: wire.name, reverse=True)
    z_wires.sort(key=lambda wire: wire.name, reverse=True)

    # Analysis based purely on my puzzle input's behaviour
    # NOT a general solution
    #
    # Incorrect bits when adding 2**something to 0
    # z10 and z11 (when 1024 + 0)
    # z18 and z19 (when 262144 + 0)
    # z24 and z25 (when 16777216 + 0)
    # z33 and z34 (when 8589934592 + 0)
    #
    # Incorrect bits when adding 2**something to itself
    # z10 and z11 (when 512 + 512)
    # z10 and z11 (when 1024 + 1024)
    # z18 and z19 (when 131072 + 131072)
    # z18 and z19 (when 262144 + 262144)
    # z24 and z25 (when 16777216 + 16777216)
    # z33 and z34 (when 4294967296 + 4294967296)

    def swap_wires(a: str, b: str):
        original_a: Wire = wires[a]
        original_b: Wire = wires[b]

        wires[b] = original_a
        original_a.name = b

        wires[a] = original_b
        original_b.name = a

    def test(x, y, print_stuff: bool = False) -> bool:
        for bit, wire in zip_longest(bin(x)[:1:-1], x_wires[::-1]):
            if bit is not None:
                wire.active = bit == "1"
            else:
                wire.active = False
        for bit, wire in zip_longest(bin(y)[:1:-1], y_wires[::-1]):
            if bit is not None:
                wire.active = bit == "1"
            else:
                wire.active = False

        if print_stuff:
            print(f"test({x}, {y}) = {int("".join("1" if z_wire.get_active() else "0" for z_wire in z_wires), 2) == x + y}")

            print(" " + "".join("1" if x_wire.get_active() else "0" for x_wire in x_wires))
            print(" " + "".join("1" if y_wire.get_active() else "0" for y_wire in y_wires) + " +")
            print("-" * len(z_wires))
            print("".join("1" if z_wire.get_active() else "0" for z_wire in z_wires))
            print("-" * len(z_wires))
            print(bin(int("".join("1" if z_wire.get_active() else "0" for z_wire in z_wires), 2) ^ (x + y))[2:].zfill(len(z_wires)))
            print("-" * len(z_wires))
            for i in range(len(z_wires) - 1, -1, -1):
                print(i // 10, end="")
            print()
            for i in range(len(z_wires) - 1, -1, -1):
                print(i % 10, end="")
            print("\n")

        return int("".join("1" if z_wire.get_active() else "0" for z_wire in z_wires), 2) == x + y

    def test_swap(a: str, b: str, known_wrong: list[tuple[int, int]]) -> bool:
        swap_wires(a, b)

        try:
            valid: bool = all(test(values[0], values[1]) for values in known_wrong)
        except RecursionError:
            valid = False

        # Restore original mappings
        swap_wires(a, b)

        return valid

    swapped: set[str] = set()

    # for a, b, known_wrong in [
    #     ("z10", "z11", [(1024, 0), (512, 512), (1024, 1024)]),
    #     ("z18", "z19", [(262144, 0), (131072, 131072), (262144, 262144)]),
    #     ("z24", "z25", [(16777216, 0), (16777216, 16777216)]),
    #     ("z33", "z34", [(8589934592, 0), (4294967296, 4294967296)])
    # ]:
    #     found_fix: bool = False
    #     for dependency_a in wires[a].get_dependencies():
    #         if dependency_a.name in swapped:
    #             continue
    #         elif dependency_a.gate is None:
    #             continue
    #
    #         for dependency_b in wires[b].get_dependencies():
    #             if dependency_a == dependency_b:
    #                 continue
    #             elif dependency_b.name in swapped:
    #                 continue
    #             elif dependency_b.gate is None:
    #                 continue
    #
    #             if all(test(values[0], values[1]) for values in known_wrong):
    #                 continue
    #
    #             if test_swap(dependency_a.name, dependency_b.name, known_wrong):
    #                 print(dependency_a.name, dependency_b.name)
    #                 swap_wires(dependency_a.name, dependency_b.name)
    #
    #                 swapped.add(dependency_a.name)
    #                 swapped.add(dependency_b.name)
    #                 found_fix = True
    #                 break
    #         if found_fix:
    #             break

    # for shift in range(45):
    #     test(1 << shift, 0, True)
    #     test(1 << shift, 1 << shift, True)
    #     input()

    # while True:
    #     request = input("> ")
    #     test(*map(int, request.split(",")), True)
        # if request not in wires:
        #     print("not found")
        # else:
        #     if wires[request].gate:
        #         print(" ".join(wires[request].gate))
        #     else:
        #         print(int(wires[request].active))

    # Solution heavily based on writeup by /u/LxsterGames on the subreddit
    # https://www.reddit.com/r/adventofcode/comments/1hla5ql/
    # and the comment on that post by /u/ElevatedUser
    # https://www.reddit.com/r/adventofcode/comments/1hla5ql/comment/m3kws15/

    for z_wire in z_wires[1:]:
        if z_wire.gate[1] != "XOR":
            swapped.add(z_wire.name)
    for output, wire in wires.items():
        if wire.gate and output[0] != "z":
            if wire.gate[0][0] not in "xy" or wire.gate[2][0] not in "xy":
                if wire.gate[1] == "XOR":
                    swapped.add(output)

    ands = list(filter(lambda w: w.gate and w.gate[1] == "AND", wires.values()))
    ors  = list(filter(lambda w: w.gate and w.gate[1] == "OR",  wires.values()))
    xors = list(filter(lambda w: w.gate and w.gate[1] == "XOR", wires.values()))

    for wire in xors:
        if wire.gate[0] in ["x00", "y00"] or wire.gate[2] in ["x00", "y00"]:
            continue

        if wire.gate[0][0] in "xy" and wire.gate[2][0] in "xy":
            if not any(other_wire.gate[0] == wire.name or other_wire.gate[2] == wire.name for other_wire in xors):
                swapped.add(wire.name)

    for wire in ands:
        if wire.gate[0] in ["x00", "y00"] or wire.gate[2] in ["x00", "y00"]:
            continue

        if not any(other_wire.gate[0] == wire.name or other_wire.gate[2] == wire.name for other_wire in ors):
            swapped.add(wire.name)
            print(wire.name)

    return ",".join(sorted(swapped))

def main() -> tuple[str, str]:
    puzzle_input = util.read.as_lines()

    return "The names of the eight wires involved in swaps are {}.", solve(puzzle_input)

class AOC_Tests(unittest.TestCase):
    @unittest.skip("No test cases")
    def test_ex1(self):
        pass

run(main)
