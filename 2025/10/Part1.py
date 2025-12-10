#!/usr/bin/env python3

#Advent of Code
#2025 Day 10, Part 1
#Solution by James C. (https://github.com/JamesMCo)

import os, sys
sys.path.append(os.path.abspath("../.."))
import unittest, util.read
from util.tests import run

from queue import Queue

def solve(puzzle_input: list[str]) -> int:
    def parse_machine(description: str) -> tuple[tuple[bool, ...], list[list[int]], list[int]]:
        target_lights: tuple[bool, ...] = tuple(light == "#" for light in description.split()[0][1:-1])
        buttons: list[list[int]] = [
            [int(target) for target in button[1:-1].split(",")]
            for button in description.split()[1:-1]
        ]
        joltages: list[int] = [int(req) for req in description.split()[-1][1:-1].split(",")]
        return target_lights, buttons, joltages

    def configure_lights(machine: tuple[tuple[bool, ...], list[list[int]], list[int]]) -> int:
        target_lights, buttons, _ = machine
        queue: Queue[tuple[tuple[bool, ...], int]] = Queue()
        queue.put((tuple([False] * len(target_lights)), 0))
        seen: set[tuple[bool, ...]] = set()

        while not queue.empty():
            lights, button_presses = queue.get()
            if lights in seen:
                continue
            seen.add(lights)

            if lights == target_lights:
                return button_presses
            else:
                for button in buttons:
                    new_state: tuple[bool, ...] = tuple(
                        light if i not in button else not light
                        for i, light in enumerate(lights)
                    )
                    if new_state not in seen:
                        queue.put((new_state, button_presses + 1))

        raise RuntimeError(f"Unable to solve machine\n{machine}")

    return sum(map(configure_lights, map(parse_machine, puzzle_input)))

def main() -> tuple[str, int]:
    puzzle_input = util.read.as_lines()

    return "The fewest button presses required to configure all of the indicator lights is {}.", solve(puzzle_input)

class AOC_Tests(unittest.TestCase):
    def test_ex1(self):
        return self.assertEqual(solve(["[.##.] (3) (1,3) (2) (2,3) (0,2) (0,1) {3,5,4,7}",
                                       "[...#.] (0,2,3,4) (2,3) (0,4) (0,1,2) (1,2,3,4) {7,5,12,7,2}",
                                       "[.###.#] (0,1,2,3,4) (0,3,4) (0,1,2,4,5) (1,2) {10,11,11,5,10,5}"]), 7)

if __name__ == "__main__":
    run(main)
