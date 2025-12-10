#!/usr/bin/env python3

#Advent of Code
#2025 Day 10, Part 2
#Solution by James C. (https://github.com/JamesMCo)

import os, sys
sys.path.append(os.path.abspath("../.."))
import unittest, util.read
from util.tests import run

import z3

def solve(puzzle_input: list[str]) -> int:
    def parse_machine(description: str) -> tuple[tuple[bool, ...], list[list[int]], list[int]]:
        target_lights: tuple[bool, ...] = tuple(light == "#" for light in description.split()[0][1:-1])
        buttons: list[list[int]] = [
            [int(target) for target in button[1:-1].split(",")]
            for button in description.split()[1:-1]
        ]
        joltages: list[int] = [int(req) for req in description.split()[-1][1:-1].split(",")]
        return target_lights, buttons, joltages

    def configure_joltages(machine: tuple[tuple[bool, ...], list[list[int]], list[int]]) -> int:
        _, buttons, target_joltages = machine
        button_presses = z3.Ints(" ".join(f"button{i}" for i in range(len(buttons))))
        total_presses = z3.Int("total_presses")
        optimiser = z3.Optimize()

        for i, joltage in enumerate(target_joltages):
            relevant_buttons = [button_var for button_targets, button_var in zip(buttons, button_presses) if i in button_targets]
            optimiser.add(sum(relevant_buttons) == joltage)
        for button_press in button_presses:
            optimiser.add(button_press >= 0)
        optimiser.add(total_presses == sum(button_presses))

        optimiser.minimize(total_presses)
        if optimiser.check() == z3.unsat:
            raise RuntimeError(f"Unable to solve machine\n{machine}")
        model = optimiser.model()
        return model[total_presses].as_long()

    return sum(map(configure_joltages, map(parse_machine, puzzle_input)))

def main() -> tuple[str, int]:
    puzzle_input = util.read.as_lines()

    return "The fewest button presses required to configure all of the joltage level counts is {}.", solve(puzzle_input)

class AOC_Tests(unittest.TestCase):
    def test_ex1(self):
        return self.assertEqual(solve(["[.##.] (3) (1,3) (2) (2,3) (0,2) (0,1) {3,5,4,7}",
                                       "[...#.] (0,2,3,4) (2,3) (0,4) (0,1,2) (1,2,3,4) {7,5,12,7,2}",
                                       "[.###.#] (0,1,2,3,4) (0,3,4) (0,1,2,4,5) (1,2) {10,11,11,5,10,5}"]), 33)

if __name__ == "__main__":
    run(main)
