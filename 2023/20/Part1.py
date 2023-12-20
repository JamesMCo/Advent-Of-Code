#!/usr/bin/env python3

#Advent of Code
#2023 Day 20, Part 1
#Solution by James C. (https://github.com/JamesMCo)

import os, sys
sys.path.append(os.path.abspath("../.."))
import unittest, util.read
from util.tests import run

from collections import deque
import re
import typing as t

def solve(puzzle_input: list[str]) -> int:
    modules: dict[str, "Module"] = {}
    pulse_queue: deque[tuple["Module", "Module", bool]] = deque()

    class Module:
        name: str
        _output_names: list[str]

        inputs: list[t.Self]
        outputs: list[t.Self]

        module_pattern: re.Pattern = re.compile(r"[%&]?(\w+) -> (.*)")

        def __init__(self: t.Self, module_description: str) -> None:
            self.name, outputs = self.module_pattern.match(module_description).groups()
            self._output_names = outputs.split(", ")

            self.inputs = []
            self.outputs = []

            modules[self.name] = self

        def register_input(self: t.Self, other: t.Self) -> None:
            self.inputs.append(other)

        def register_outputs(self: t.Self) -> None:
            for output_name in self._output_names:
                output: t.Self = modules[output_name] if output_name in modules else Module(f"{output_name} -> ")
                self.outputs.append(output)
                output.register_input(self)

        def receive_pulse(self: t.Self, module: t.Self, pulse_is_high: bool) -> None:
            # Untyped module just receives pulses, doesn't pass any on
            pass

    class FlipFlopModule(Module):
        state: bool

        def __init__(self: t.Self, module_description: str) -> None:
            super().__init__(module_description)
            self.state = False

        @t.override
        def receive_pulse(self: t.Self, module: Module, pulse_is_high: bool) -> None:
            if pulse_is_high:
                # High pulses are ignored
                pass
            else:
                # Low pulses flip the state and send a pulse (high if now on, low if now off)
                self.state = not self.state
                for module in self.outputs:
                    pulse_queue.append((self, module, self.state))

    class ConjunctionModule(Module):
        last_received: dict[str, bool]

        def __init__(self: t.Self, module_description: str) -> None:
            super().__init__(module_description)
            self.last_received = {}

        @t.override
        def register_input(self: t.Self, other: t.Self) -> None:
            self.inputs.append(other)
            self.last_received[other.name] = False

        @t.override
        def receive_pulse(self: t.Self, module: Module, pulse_is_high: bool) -> None:
            self.last_received[module.name] = pulse_is_high
            if all(self.last_received.values()):
                # If all remembered inputs are high pulses, send a low pulse
                for module in self.outputs:
                    pulse_queue.append((self, module, False))
            else:
                # If all remembered inputs are not high pulses, send a high pulse
                for module in self.outputs:
                    pulse_queue.append((self, module, True))

    class BroadcastModule(Module):
        @t.override
        def receive_pulse(self: t.Self, module: Module, pulse_is_high: bool) -> None:
            # Rebroadcast all incoming pulses to outputs unchanged
            for module in self.outputs:
                pulse_queue.append((self, module, pulse_is_high))

    for line in puzzle_input:
        if line[0] == "%":
            FlipFlopModule(line)
        elif line[0] == "&":
            ConjunctionModule(line)
        elif line.startswith("broadcaster "):
            BroadcastModule(line)
        else:
            Module(line)
    for m in list(modules.values()):
        m.register_outputs()

    button = Module("button -> broadcaster")
    low_pulses, high_pulses = 0, 0
    for _ in range(1000):
        pulse_queue.append((button, modules["broadcaster"], False))

        while pulse_queue:
            from_module: Module
            to_module: Module
            pulse: bool
            from_module, to_module, pulse = pulse_queue.popleft()

            if pulse:
                high_pulses += 1
            else:
                low_pulses += 1

            to_module.receive_pulse(from_module, pulse)

    return low_pulses * high_pulses

def main() -> tuple[str, int]:
    puzzle_input = util.read.as_lines()

    return "The product of the total number of low pulses and high pulses sent is {}.", solve(puzzle_input)

class AOC_Tests(unittest.TestCase):
    def test_ex1(self):
        return self.assertEqual(solve(["broadcaster -> a, b, c",
                                       "%a -> b",
                                       "%b -> c",
                                       "%c -> inv",
                                       "&inv -> a"]), 32000000)

    def test_ex2(self):
        return self.assertEqual(solve(["broadcaster -> a",
                                       "%a -> inv, con",
                                       "&inv -> b",
                                       "%b -> con",
                                       "&con -> output"]), 11687500)

run(main)
